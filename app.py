
import firebase_admin
import os
from firebase_admin import credentials, firestore, auth
from flask_wtf.csrf import CSRFProtect


cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
# 建立資料庫的實例(db)
db = firestore.client()

import time
import datetime

# 引用flask相關資源
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, abort
# 引用各種表單類別
# 引用自行建立的functions
from recordFunctions import historyRecord, recordTrace, oneDayRecord, oneMonRecord
from settingFunction import get_account_list, get_items_list, modify_list
from calculateFunction import calculateTableContent, get_account_detail, get_income_detail, get_expense_detail, digitComma

app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)

# Custom filter
app.jinja_env.filters["digitComma"] = digitComma


# 設定應用程式的SECRET_KEY
app.config['SECRET_KEY'] = 'abc12345678'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
cookie_name = 'flask_cookie'



@app.context_processor
def check_login():
    print("[check_login]")
    # 取得session_cookie
    session_cookie = request.cookies.get(cookie_name)
    #print("[session_cookie]", session_cookie)
    # 預設登入狀態
    auth_state = {
        # 是否登入
        "is_login": False,
        # 是否為管理者
        "is_admin": False,
        # 資料
        "user": {}
    }
    # 準備驗證
    try:
        # 驗證session_cookie
        user_info = auth.verify_session_cookie(session_cookie, check_revoked=True)
        # 將資料存到登入狀態內
        auth_state["user"] = user_info
        # 取得user email
        user_email = user_info['email']
        
        # 取得 admin_list/{email} 文件
        #admin_doc = db.document(f'admin_list/{user_email}').get()
        
        # 判斷admin_doc是否存在
        #if admin_doc.exists:
        #    auth_state["is_admin"] = True

        # 標記此人為登入狀態
        auth_state["is_login"] = True

        
    except:
        # 未登入
        print('[User not login]')
    # 把auth_state傳遞到各個模板內
    return dict(auth_state=auth_state)

@app.before_request
def guard():
    auth_state = check_login()['auth_state']
    # 指向使用者所導入的路由函數名稱
    endpoint = request.endpoint
    is_admin = auth_state['is_admin']
    # 受管理者權限保護的頁面
    admin_route_list = [
        'create_product_page',
        'edit_product_page'
    ]
    # 如果造訪的頁面是
    # 管理者權限保護頁面，而且此人並非管理者
    if endpoint in admin_route_list and not is_admin:
        # 強制回首頁
        return redirect('/')


month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

@app.route('/', methods=['GET', 'POST'])
def index_page():

    try:
        # get user email and use for database naming
        session_cookie = request.cookies.get(cookie_name)
        #print("[session_cookie]", session_cookie)
        user_info = auth.verify_session_cookie(session_cookie, check_revoked=True)
        user_email = user_info['email']
        user_email = user_email.split("@")[0]

            # now use temp data to show on index.html
        record_now = datetime.datetime.now()
        year_now = record_now.year
        month_now = record_now.month
        day_now = record_now.day
        record_date = str(year_now) + "." + str(month_now) + "." + str(day_now)
        # To keep hour, minute, second in 2 digit form when changeing to string type
        record_time = record_now.strftime("%H") + ":" + record_now.strftime("%M") + ":" + record_now.strftime("%S")

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        record_date_yesterday = str(yesterday.year) + "." + str(yesterday.month) + "." + str(yesterday.day)
        #print(record_date)
        #print(record_date_yesterday)

        # get account and items of income/expense from database
        Account = get_account_list(year_now, user_email)
        incomeItem, expendItem = get_items_list(year_now, user_email)

        # variables for transType
        income_var = "Income"
        expense_var = "Expense"
        transfer_var = "Transfer"

        if request.method == 'GET':
            
            # 取得當天與前一天的資料，藉由oneDayRecord function
            income_today_list = oneDayRecord(year_now, month_now, record_date, income_var, user_email)
            expense_today_list = oneDayRecord(year_now, month_now, record_date, expense_var, user_email)
            transfer_today_list = oneDayRecord(year_now, month_now, record_date, transfer_var, user_email)
            
            income_yesterday_list = oneDayRecord(year_now, month_now, record_date_yesterday, income_var, user_email)
            expense_yesterday_list = oneDayRecord(year_now, month_now, record_date_yesterday, expense_var, user_email)
            transfer_yesterday_list = oneDayRecord(year_now, month_now, record_date_yesterday, transfer_var, user_email)

            
            return render_template('index.html', incomeItem=incomeItem, expendItem=expendItem, Account=Account, month_list=month_list, \
                                    income_today_list=income_today_list, expense_today_list=expense_today_list, transfer_today_list=transfer_today_list, \
                                    income_yesterday_list=income_yesterday_list, expense_yesterday_list=expense_yesterday_list, transfer_yesterday_list=transfer_yesterday_list )
        
        # 取得Add item的post data
        if request.method == "POST" and "transactionType" in request.get_json() and "editButton" not in request.get_json():
            historyRecord(year_now, month_now, month_list, user_email)
            # 取得newItem_modal的輸入資料，並且將對應資料分別存到不同的data list中(額外利用python datatime加上時間紀錄)
            transType = request.get_json()['transactionType'] 
            
            # 利用transType & 輸入資料時的年/月/日作為資料庫的路徑分配
            if transType == income_var:
                # 呼叫recordTrace函式，判斷提交內容是當天的第幾筆資料
                record_count = recordTrace(record_date, record_time, transType, user_email)

                #print(f"item name check: {request.get_json()['incomeItem']}")
                income_quick_record = {
                    'transType': transType,
                    'month': request.get_json()['month'],
                    'incomeItem': request.get_json()['incomeItem'],
                    'money': request.get_json()['amountOfMoney'],
                    'incomeAccount' : request.get_json()['incomeAccount'],
                    'incomeNote': request.get_json()['incomeNote'],
                    'recordDate': record_date,
                    'recordTime': record_time,
                    'recordCount': record_count
                }
                # 將資料寫入對應的document路徑，並將當天不同筆的數量資訊標示在document name做區隔
                #doc_ref = db.collection(transType).document("YY" + str(year_now)).collection("MM" + str(month_now)).document("DD" + str(day_now) + "_" + str(record_count))
                doc_ref = db.collection(user_email).document("Record").collection(transType).document("YY" + str(year_now)).collection("MM" + str(month_now)).document("DD" + str(day_now) + "_" + str(record_count))
                doc_ref.set(income_quick_record)

            elif transType == expense_var:
                record_count = recordTrace(record_date, record_time, transType, user_email)

                expense_quick_record = {
                    'transType': transType,
                    'month': request.get_json()['month'],
                    'expendItem': request.get_json()['expendItem'],
                    'money': request.get_json()['amountOfMoney'],
                    'expendAccount' : request.get_json()['expendAccount'],
                    'expendNote': request.get_json()['expendNote'],
                    'recordDate': record_date,
                    'recordTime': record_time,
                    'recordCount': record_count
                }

                #doc_ref = db.collection(transType).document("YY" + str(year_now)).collection("MM" + str(month_now)).document("DD" + str(day_now) + "_" + str(record_count))
                doc_ref = db.collection(user_email).document("Record").collection(transType).document("YY" + str(year_now)).collection("MM" + str(month_now)).document("DD" + str(day_now) + "_" + str(record_count))
                doc_ref.set(expense_quick_record)
                
            elif transType == transfer_var:
                record_count = recordTrace(record_date, record_time, transType, user_email)

                transfer_quick_record = {
                    'transType': transType,
                    'month': request.get_json()['month'],
                    'withdrawAccount': request.get_json()['withdrawAccount'],
                    'transAmount': request.get_json()['transAmount'],
                    'depositAccount': request.get_json()['depositAccount'],
                    'transNote': request.get_json()['transNote'],
                    'recordDate': record_date,
                    'recordTime': record_time,
                    'recordCount': record_count
                }

                #doc_ref = db.collection(transType).document("YY" + str(year_now)).collection("MM" + str(month_now)).document("DD" + str(day_now) + "_" + str(record_count))
                doc_ref = db.collection(user_email).document("Record").collection(transType).document("YY" + str(year_now)).collection("MM" + str(month_now)).document("DD" + str(day_now) + "_" + str(record_count))
                doc_ref.set(transfer_quick_record)

            return redirect(url_for("/"))
        
        # 取得edit的post data
        if request.method == "POST" and "transactionType" in request.get_json() and "editButton" in request.get_json():
            transType = request.get_json()['transactionType'] 
            editCount = request.get_json()['recordCount']
            editDate = request.get_json()['recordDate']
            editTime = request.get_json()['recordTime']
            editDate_split = editDate.split(".")

            if transType == income_var:
                update_income_record = {
                    'month': request.get_json()['month'],
                    'incomeItem': request.get_json()['incomeItem'],
                    'money': request.get_json()['amountOfMoney'],
                    'incomeAccount' : request.get_json()['incomeAccount'],
                    'incomeNote': request.get_json()['incomeNote']
                }
                #doc_ref = db.collection(transType).document("YY" + editDate_split[0]).collection("MM" + editDate_split[1]).document("DD" + editDate_split[2] + "_" + str(editCount))
                doc_ref = db.collection(user_email).document("Record").collection(transType).document("YY" + editDate_split[0]).collection("MM" + editDate_split[1]).document("DD" + editDate_split[2] + "_" + str(editCount))
                doc_ref.set(update_income_record, merge=True) # update data by set()

            elif transType == expense_var:
                update_expend_record = {
                    'month': request.get_json()['month'],
                    'expendItem': request.get_json()['expendItem'],
                    'money': request.get_json()['amountOfMoney'],
                    'expendAccount' : request.get_json()['expendAccount'],
                    'expendNote': request.get_json()['expendNote']
                }
                #doc_ref = db.collection(transType).document("YY" + editDate_split[0]).collection("MM" + editDate_split[1]).document("DD" + editDate_split[2] + "_" + str(editCount))
                doc_ref = db.collection(user_email).document("Record").collection(transType).document("YY" + editDate_split[0]).collection("MM" + editDate_split[1]).document("DD" + editDate_split[2] + "_" + str(editCount))
                doc_ref.set(update_expend_record, merge=True)
            
            elif transType == transfer_var:
                #editCount = request.get_json()['recordCount']
                update_transfer_record = {
                    'month': request.get_json()['month'],
                    'withdrawAccount': request.get_json()['withdrawAccount'],
                    'transAmount': request.get_json()['transAmount'],
                    'depositAccount': request.get_json()['depositAccount'],
                    'transNote': request.get_json()['transNote']
                }
                #doc_ref = db.collection(transType).document("YY" + editDate_split[0]).collection("MM" + editDate_split[1]).document("DD" + editDate_split[2] + "_" + str(editCount))
                doc_ref = db.collection(user_email).document("Record").collection(transType).document("YY" + editDate_split[0]).collection("MM" + editDate_split[1]).document("DD" + editDate_split[2] + "_" + str(editCount))
                doc_ref.set(update_transfer_record, merge=True)

            return redirect(url_for("/"))

        # 取得delete的post data
        if request.method == "POST" and "deleteButton" in request.get_json(): 
            deleteType = request.get_json()['transType']
            deleteCount = request.get_json()['recordCount']
            deleteDate = request.get_json()['recordDate']
            #deleteTime = request.get_json()['recordTime']
            
            deleteDate_split = deleteDate.split(".")    
        
            # find corresponding document and delete it
            #doc_ref = db.collection(deleteType).document("YY" + deleteDate_split[0]).collection("MM" + deleteDate_split[1]).document("DD" + deleteDate_split[2] + "_" + str(deleteCount))
            doc_ref = db.collection(user_email).document("Record").collection(deleteType).document("YY" + deleteDate_split[0]).collection("MM" + deleteDate_split[1]).document("DD" + deleteDate_split[2] + "_" + str(deleteCount))
            doc_ref.delete() 
            #print(delete_item.to_dict())
            
            return redirect(url_for("/"))


    except:
        print("[User not login]")
        return render_template('index.html')


    


@app.route('/account_book', methods=['GET', 'POST'])
def account_book():
    # get user email and use for database naming
    session_cookie = request.cookies.get(cookie_name)
    user_info = auth.verify_session_cookie(session_cookie, check_revoked=True)
    user_email = user_info['email']
    user_email = user_email.split("@")[0]

    record_now = datetime.datetime.now()
    year_now = record_now.year
    month_now = record_now.month
    day_now = record_now.day

    ### Create specific date for test
    #create_date = datetime.date(2021, 10, 11)
    #year_now = create_date.year
    #month_now = create_date.month
    #day_now = create_date.day
    ############################

    # get account and items of income/expense from database
    Account = get_account_list(year_now, user_email)
    incomeItem, expendItem = get_items_list(year_now, user_email)

    record_date = str(year_now) + "." + str(month_now) + "." + str(day_now)
    # To keep hour, minute, second in 2 digit form when changeing to string type
    record_time = record_now.strftime("%H") + ":" + record_now.strftime("%M") + ":" + record_now.strftime("%S")
    
    # variables for transType
    income_var = "Income"
    expense_var = "Expense"
    transfer_var = "Transfer"
    
    if request.method == 'GET':
        
        # get history data for select bar
        historyRecord_doc = db.collection(user_email).document("Record").collection("history_record").document("data").get()
        historyRecord_data = historyRecord_doc.to_dict()

        record_request = request.args.get('selected_data')
        #print(record_request)
        
        income_month_list = []
        expense_month_list = []
        transfer_month_list = []
        year_title = ''
        month_title = ''

        # default狀態:顯示當月資料
        if not record_request:
            income_month_list = oneMonRecord(year_now, month_now, income_var, user_email)
            expense_month_list = oneMonRecord(year_now, month_now, expense_var, user_email)
            transfer_month_list = oneMonRecord(year_now, month_now, transfer_var, user_email)
            year_title = str(year_now)
            month_title = str(month_now)
        # 經由ajax傳遞選訂的年份跟月份，回傳不同的data回account table
        else:
            select_year, select_month = record_request.split(" ")
            income_month_list = oneMonRecord(int(select_year), int(select_month), income_var, user_email)
            expense_month_list = oneMonRecord(int(select_year), int(select_month), expense_var, user_email)
            transfer_month_list = oneMonRecord(int(select_year), int(select_month), transfer_var, user_email)
            year_title = select_year
            month_title = select_month
     

        return render_template('account_book.html', incomeItem=incomeItem, expendItem=expendItem, Account=Account, month_list=month_list, \
            income_month_list=income_month_list, expense_month_list=expense_month_list, transfer_month_list=transfer_month_list, year_title=year_title, month_title=month_title, \
            historyRecord_data=historyRecord_data)
    
    # 取得record form的post data
    if request.method == "POST" and "transactionType_book_1" in request.get_json() and "editButton_book" not in request.get_json():
        historyRecord(year_now, month_now, month_list, user_email)
        print("url check")
        # collect all record separate by id_num
        for id_num in range(1, 6):
            transType_string = 'transactionType_book_' + str(id_num)
            if transType_string in request.get_json():
                transType = request.get_json()[transType_string] 

                # 利用transType & 輸入資料時的年/月/日作為資料庫的路徑分配
                if transType == income_var:
                    # 呼叫recordTrace函式，判斷提交內容是當天的第幾筆資料
                    record_count = recordTrace(record_date, record_time, transType, user_email)

                    #string with id_num for requesting income data 
                    month_book = 'month_book_' + str(id_num)
                    incomeItem_book = 'incomeItem_book_' + str(id_num)
                    amountOfMoney_book = 'amountOfMoney_book_' + str(id_num)
                    incomeAccount_book = 'incomeAccount_book_' + str(id_num)
                    incomeNote_book = 'incomeNote_book_' + str(id_num)

                    income_quick_record = {
                        'transType': transType,
                        'month': request.get_json()[month_book],
                        'incomeItem': request.get_json()[incomeItem_book],
                        'money': request.get_json()[amountOfMoney_book],
                        'incomeAccount' : request.get_json()[incomeAccount_book],
                        'incomeNote': request.get_json()[incomeNote_book],
                        'recordDate': record_date,
                        'recordTime': record_time,
                        'recordCount': record_count
                    }
                    # 將資料寫入對應的document路徑，並將當天不同筆的數量資訊標示在document name做區隔
                    #doc_ref = db.collection(transType).document("YY" + str(year_now)).collection("MM" + str(month_now)).document("DD" + str(day_now) + "_" + str(record_count))
                    doc_ref = db.collection(user_email).document("Record").collection(transType).document("YY" + str(year_now)).collection("MM" + str(month_now)).document("DD" + str(day_now) + "_" + str(record_count))
                    doc_ref.set(income_quick_record)

                elif transType == expense_var:
                    record_count = recordTrace(record_date, record_time, transType, user_email)

                    #string with id_num for requesting expense data 
                    month_book = 'month_book_' + str(id_num)
                    expendItem_book = 'expendItem_book_' + str(id_num)
                    amountOfMoney_book = 'amountOfMoney_book_' + str(id_num)
                    expendAccount_book = 'expendAccount_book_' + str(id_num)
                    expendNote_book = 'expendNote_book_' + str(id_num)

                    expense_quick_record = {
                        'transType': transType,
                        'month': request.get_json()[month_book],
                        'expendItem': request.get_json()[expendItem_book],
                        'money': request.get_json()[amountOfMoney_book],
                        'expendAccount' : request.get_json()[expendAccount_book],
                        'expendNote': request.get_json()[expendNote_book],
                        'recordDate': record_date,
                        'recordTime': record_time,
                        'recordCount': record_count
                    }

                    #doc_ref = db.collection(transType).document("YY" + str(year_now)).collection("MM" + str(month_now)).document("DD" + str(day_now) + "_" + str(record_count))
                    doc_ref = db.collection(user_email).document("Record").collection(transType).document("YY" + str(year_now)).collection("MM" + str(month_now)).document("DD" + str(day_now) + "_" + str(record_count))
                    doc_ref.set(expense_quick_record)
                    
                elif transType == transfer_var:
                    record_count = recordTrace(record_date, record_time, transType, user_email)

                    #string with id_num for requesting income data 
                    month_book = 'month_book_' + str(id_num)
                    withdrawAccount_book = 'withdrawAccount_book_' + str(id_num)
                    transAmount_book = 'transAmount_book_' + str(id_num)
                    depositAccount_book = 'depositAccount_book_' + str(id_num)
                    transNote_book = 'transNote_book_' + str(id_num)

                    transfer_quick_record = {
                        'transType': transType,
                        'month': request.get_json()[month_book],
                        'withdrawAccount': request.get_json()[withdrawAccount_book],
                        'transAmount': request.get_json()[transAmount_book],
                        'depositAccount': request.get_json()[depositAccount_book],
                        'transNote': request.get_json()[transNote_book],
                        'recordDate': record_date,
                        'recordTime': record_time,
                        'recordCount': record_count
                    }

                    #doc_ref = db.collection(transType).document("YY" + str(year_now)).collection("MM" + str(month_now)).document("DD" + str(day_now) + "_" + str(record_count))
                    doc_ref = db.collection(user_email).document("Record").collection(transType).document("YY" + str(year_now)).collection("MM" + str(month_now)).document("DD" + str(day_now) + "_" + str(record_count))
                    doc_ref.set(transfer_quick_record)

        return redirect(url_for("/account_book"))
    
    # get data from edit accountBook record
    if request.method == "POST" and "editButton_book" in request.get_json():
        transType = request.get_json()['transactionType'] 
        editCount = request.get_json()['recordCount']
        editDate = request.get_json()['recordDate']
        editTime = request.get_json()['recordTime']
        editDate_split = editDate.split(".")

        if transType == income_var:
            update_income_record = {
                'month': request.get_json()['month'],
                'incomeItem': request.get_json()['incomeItem'],
                'money': request.get_json()['amountOfMoney'],
                'incomeAccount' : request.get_json()['incomeAccount'],
                'incomeNote': request.get_json()['incomeNote']
            }
            #doc_ref = db.collection(transType).document("YY" + editDate_split[0]).collection("MM" + editDate_split[1]).document("DD" + editDate_split[2] + "_" + str(editCount))
            doc_ref = db.collection(user_email).document("Record").collection(transType).document("YY" + editDate_split[0]).collection("MM" + editDate_split[1]).document("DD" + editDate_split[2] + "_" + str(editCount))
            doc_ref.set(update_income_record, merge=True) # update data by set()

        elif transType == expense_var:
            update_expend_record = {
                'month': request.get_json()['month'],
                'expendItem': request.get_json()['expendItem'],
                'money': request.get_json()['amountOfMoney'],
                'expendAccount' : request.get_json()['expendAccount'],
                'expendNote': request.get_json()['expendNote']
            }
            #doc_ref = db.collection(transType).document("YY" + editDate_split[0]).collection("MM" + editDate_split[1]).document("DD" + editDate_split[2] + "_" + str(editCount))
            doc_ref = db.collection(user_email).document("Record").collection(transType).document("YY" + editDate_split[0]).collection("MM" + editDate_split[1]).document("DD" + editDate_split[2] + "_" + str(editCount))
            doc_ref.set(update_expend_record, merge=True)
        
        elif transType == transfer_var:
            #editCount = request.get_json()['recordCount']
            update_transfer_record = {
                'month': request.get_json()['month'],
                'withdrawAccount': request.get_json()['withdrawAccount'],
                'transAmount': request.get_json()['transAmount'],
                'depositAccount': request.get_json()['depositAccount'],
                'transNote': request.get_json()['transNote']
            }
            #doc_ref = db.collection(transType).document("YY" + editDate_split[0]).collection("MM" + editDate_split[1]).document("DD" + editDate_split[2] + "_" + str(editCount))
            doc_ref = db.collection(user_email).document("Record").collection(transType).document("YY" + editDate_split[0]).collection("MM" + editDate_split[1]).document("DD" + editDate_split[2] + "_" + str(editCount))
            doc_ref.set(update_transfer_record, merge=True)

        return redirect(url_for("account_book"))

    # get data from delete accountBook record
    if request.method == "POST" and "deleteButton_book" in request.get_json():
        deleteType = request.get_json()['transType']
        deleteCount = request.get_json()['recordCount']
        deleteDate = request.get_json()['recordDate']
        #deleteTime = request.get_json()['recordTime']
        
        deleteDate_split = deleteDate.split(".")    
    
        # find corresponding document and delete it
        #doc_ref = db.collection(deleteType).document("YY" + deleteDate_split[0]).collection("MM" + deleteDate_split[1]).document("DD" + deleteDate_split[2] + "_" + str(deleteCount))
        doc_ref = db.collection(user_email).document("Record").collection(deleteType).document("YY" + deleteDate_split[0]).collection("MM" + deleteDate_split[1]).document("DD" + deleteDate_split[2] + "_" + str(deleteCount))
        doc_ref.delete() 
        #print(delete_item.to_dict())
        
        return redirect(url_for("/account_book"))


@app.route('/account_manage', methods=['GET', 'POST'])
def account_manage():
    # get user email and use for database naming
    session_cookie = request.cookies.get(cookie_name)
    user_info = auth.verify_session_cookie(session_cookie, check_revoked=True)
    user_email = user_info['email']
    user_email = user_email.split("@")[0]

    record_now = datetime.datetime.now()
    year_now = record_now.year

    if request.method == 'GET':
        # get history data for select bar
        historyRecord_doc = db.collection(user_email).document("Record").collection("history_record").document("data").get()
        historyRecord_data = historyRecord_doc.to_dict()

        # get account and items of income/expense from database
        Account = get_account_list(year_now, user_email)
        incomeItem, expendItem = get_items_list(year_now, user_email)

        record_request = request.args.get('selected_data')
        #print(record_request)

        # default狀態:顯示當年統計資料
        all_account_dict = {}
        if not record_request:
            calculateTableContent('', '', str(year_now), Account, user_email)

            all_account_dict = get_account_detail(Account, year_now, user_email)
            all_income_dict = get_income_detail(incomeItem, year_now, user_email)
            all_expense_dict = get_expense_detail(expendItem, year_now, user_email)
            year_title = str(year_now)
        # 經由ajax傳遞選訂的年份，回傳不同年份的data回account manage table
        else:
            selected_year = int(record_request)
            calculateTableContent('', '', str(selected_year), Account, user_email)

            all_account_dict = get_account_detail(Account, selected_year, user_email)
            all_income_dict = get_income_detail(incomeItem, selected_year, user_email)
            all_expense_dict = get_expense_detail(expendItem, selected_year, user_email)
            year_title = record_request        

        return render_template('account_manage.html', incomeItem=incomeItem, expendItem=expendItem, Account=Account, month_list=month_list, \
                                all_account_dict=all_account_dict, all_income_dict=all_income_dict, all_expense_dict=all_expense_dict, historyRecord_data=historyRecord_data, \
                                year_title=year_title)
    
    if request.method == 'POST':
        Account = get_account_list(year_now, user_email)
        originalDeposit = request.get_json()['Original_deposit']
        selected_year = request.get_json()['selected_year']
        selected_account_name = request.get_json()['account_name']
        calculateTableContent(selected_account_name, originalDeposit, selected_year, Account, user_email)

        return redirect(url_for("account_manage"))

@app.route('/account_setting', methods=['GET', 'POST'])
def account_setting():
    # get user email and use for database naming
    session_cookie = request.cookies.get(cookie_name)
    user_info = auth.verify_session_cookie(session_cookie, check_revoked=True)
    user_email = user_info['email']
    user_email = user_email.split("@")[0]

    record_now = datetime.datetime.now()
    year_now = record_now.year

    if request.method == 'GET':
        # get account and items of income/expense from database
        Account = get_account_list(year_now, user_email)
        incomeItem, expendItem = get_items_list(year_now, user_email)

        return render_template('setting.html', incomeItem=incomeItem, expendItem=expendItem, Account=Account)
    
    if request.method == 'POST':
        form_type = request.get_json()['form_type']
        delete_list = request.get_json()['delete_list']
        add_list = request.get_json()['add_list']

        modify_list(form_type, delete_list, add_list, year_now, user_email)
        return redirect(url_for("account_setting"))
    

@app.route('/api/login', methods=['POST'])
def login():
    print('準備開始登入API流程')
    # 取得前端傳給後端的資料
    id_Token = request.json['idToken']
    print('[id_token]', id_Token)

    # 過期日
    expires_in = datetime.timedelta(days=7)
    try:
        # 產生session_cookie
        session_cookie = auth.create_session_cookie(id_Token, expires_in=expires_in)
        #print('[session_cookie]', session_cookie)
        # 準備要回應給前端JS的資訊
        res = jsonify({
            'msg': 'OK'
        })
        expires = datetime.datetime.now() + expires_in
        #將session_cookie寫入至使用者的瀏覽器內
        res.set_cookie(cookie_name, session_cookie, expires=expires, httponly=True)
        return res

    except:
        return abort(401, "IDToken失效或Firebase Server目前出狀況")

@app.route('/api/logout', methods=['POST'])
def logout():
    # 讓指定的cookie失效
    res = jsonify({ 'msg': 'OK'})
    res.set_cookie(cookie_name, expires=0)
    return res


if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    dev_host = '127.0.0.1'
    heroku_host = '0.0.0.0'

    # 應用程式開始運行
    app.run(debug=True, host=heroku_host, port=port)
