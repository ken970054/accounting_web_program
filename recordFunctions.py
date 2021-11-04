
from firebase_admin import firestore

import time

db = firestore.client()


# variables for transType
income_var = "Income"
expense_var = "Expense"
transfer_var = "Transfer"

# 比較提交時間（確定是否在同一天），並且追蹤當天提交筆數
def recordTrace(record_date, record_time, transType, user_email):
    #date_ref = db.collection("previous_record").document("data")
    date_ref = db.collection(user_email).document("Record").collection("previous_record").document("data")

    try:
        previous_data = date_ref.get().to_dict()

        # 若還在當天的資料，維持record數量並return
        if time.strptime(previous_data['previous_date'], "%Y.%m.%d") == time.strptime(record_date, "%Y.%m.%d"): 
            current_count = previous_data[transType + 'Count'] + 1
            doc = {
                transType + 'Count': current_count,
                'previous_date': record_date,
                'previous_time': record_time
            }
            date_ref.update(doc) 
            return current_count

        # 若為新的一天的資料，重置record數量為0並return
        else:
            if transType == income_var:
                doc = {
                    'IncomeCount': 1,
                    'ExpenseCount': 0,
                    'TransferCount': 0,
                    'previous_date': record_date ,
                    'previous_time': record_time
                }
                date_ref.update(doc)
                return 1
            elif transType == expense_var:
                doc = {
                    'IncomeCount': 0,
                    'ExpenseCount': 1,
                    'TransferCount': 0,
                    'previous_date': record_date ,
                    'previous_time': record_time
                }
                date_ref.update(doc)
                return 1
            elif transType == transfer_var:
                doc = {
                    'IncomeCount': 0,
                    'ExpenseCount': 0,
                    'TransferCount': 1,
                    'previous_date': record_date,
                    'previous_time': record_time
                }
                date_ref.update(doc)
                return 1
    
    # Initialization: 避免還沒存過資料遇到的錯誤
    except:
        if transType == income_var:
            doc = {
                'IncomeCount': 1,
                'ExpenseCount': 0,
                'TransferCount': 0,
                'previous_date': record_date,
                'previous_time': record_time
            }
            date_ref.set(doc)
            return 1
        elif transType == expense_var:
            doc = {
                'IncomeCount': 0,
                'ExpenseCount': 1,
                'TransferCount': 0,
                'previous_date': record_date, 
                'previous_time': record_time
            }
            date_ref.set(doc)
            return 1
        elif transType == transfer_var:
            doc = {
                'IncomeCount': 0,
                'ExpenseCount': 0,
                'TransferCount': 1,
                'previous_date': record_date,
                'previous_time': record_time
            }
            date_ref.set(doc)
            return 1


def oneDayRecord(record_year, record_month, record_date, transType, user_email):
    record_list = []
    #record_today = db.collection(transType).document("YY" + str(record_year)).collection("MM" + str(record_month)).where('recordDate', '==', record_date)
    record_today = db.collection(user_email).document("Record").collection(transType).document("YY" + str(record_year)).collection("MM" + str(record_month)).where('recordDate', '==', record_date)

    try:
        record_data_today = record_today.get()
        for data in record_data_today:
            #print(f"文件內容: {data.to_dict()}")
            each_record = data.to_dict()
            record_list.append(each_record)
    except:
        record_list = []

    return record_list 


def oneMonRecord(record_year, record_month, transType, user_email):
    record_list = []
    #record_month = db.collection(transType).document("YY" + str(record_year)).collection("MM" + str(record_month))
    record_month = db.collection(user_email).document("Record").collection(transType).document("YY" + str(record_year)).collection("MM" + str(record_month))

    try:
        record_data_today = record_month.get()
        for data in record_data_today:
            #print(f"文件內容: {data.to_dict()}")
            each_record = data.to_dict()
            record_list.append(each_record)
    except:
        record_list = []

    return record_list 



def historyRecord(record_year, record_month, month_list, user_email):
    year = str(record_year)
    month_num = str(record_month)
    month_string = month_list[record_month - 1]
    month_dict = {month_num: month_string}
    print(user_email)
    #record_history = db.collection('history_record').document("data")
    record_history = db.collection(user_email).document("Record").collection('history_record').document("data")
    
    record_history_data = record_history.get()
    record_history_dict = record_history_data.to_dict()

    if record_history_dict:
        if year in record_history_dict:
            if month_dict not in record_history_dict[year]:
                record_history_dict[year].append(month_dict) #年份存在，月份不存在，需要存入新的月份
                record_history.update({year: record_history_dict[year]})
        else:
            record_history.update({year: [month_dict]}) #年份不存在，存入新的年份跟對應月份
    else:
        print("NONE")
        doc = {
            year: [month_dict]
        }
        record_history.set(doc)
