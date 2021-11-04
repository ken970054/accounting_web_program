
from firebase_admin import firestore

import time

db = firestore.client()


# variables for transType
income_var = "Income"
expense_var = "Expense"
transfer_var = "Transfer"

# get account/asset list or set default for html use
def get_account_list(year, user_email):
    last_year = year - 1
    last_year = str(last_year)
    year = str(year)
    month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    account_ref = db.collection(user_email).document("Record").collection("yourAccount").document("list")
    account_dict = account_ref.get().to_dict()
    
    default_Account_list = ["Cash", "Salary Bank", "Credit Card Bank", "Investment Bank"]
    

    # 剛創立帳號時，先儲存default的內容進去
    if not account_dict:
        account_dict = {}
        for account in default_Account_list:
            account_dict[account] = account
            # 建立default account document，給後續記帳record使用
            account_doc = db.collection(user_email).document("Record").collection("yourAccount").document(account)
            account_record_dict = {year: {"Account balance": 0, "Original deposit": 0}}
            for month in month_list:
                account_record_dict[year][month] = 0
            account_doc.set(account_record_dict)

        # default account list document
        account_ref.set(account_dict) 
        return default_Account_list

    # account內容已經存在，讀取並以list的內容return給render_template
    elif account_dict:
        account_list = []
        for key, account in account_dict.items():
            # 注意：若遇到更改年份時，需要update新年份dict到firebase中，且account要沿用先前的balance值
            account_doc = db.collection(user_email).document("Record").collection("yourAccount").document(account)
            account_record_dict = account_doc.get().to_dict()
            if year not in account_record_dict:
                last_year_balance = account_record_dict[last_year]["Account balance"]
                account_record_dict = {year: {"Account balance": last_year_balance, "Original deposit": last_year_balance}}
                for month in month_list:
                    account_record_dict[year][month] = 0 
                account_doc.update(account_record_dict)
            
            # 蒐集list內容
            account_list.append(account)
        
        sorted_account_list = sorted(account_list)
        return sorted_account_list
            


# get income and expense items list or set default for html use
def get_items_list(year, user_email):
    year = str(year)
    month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    incomeItem_ref = db.collection(user_email).document("Record").collection("incomeItem").document("list")
    expenseItem_ref = db.collection(user_email).document("Record").collection("expenseItem").document("list")
    incomeItem_dict = incomeItem_ref.get().to_dict()
    expenseItem_dict = expenseItem_ref.get().to_dict()

    default_incomeItem_list = ["Salary", "Bonus", "Investment interest", "Part-time", "Others"]
    default_expenseItem_list = ["Dining", "Clothing", "Internet & Phone", "Insurance", "Transportation", "Vehicle maintenance", "Education", "Rent", "Health care", "Daily Necessities", "Entertainment", "Book", "Donation", "Tax", "Others"]
    

    ## 剛創立帳號時，先儲存income and expense item的default內容進去 ##
    if not incomeItem_dict and not expenseItem_dict:
        incomeItem_dict = {}
        for income_item in default_incomeItem_list:
            incomeItem_dict[income_item] = income_item
            # 建立default income document，給後續記帳record使用
            income_doc = db.collection(user_email).document("Record").collection("incomeItem").document(income_item)
            income_record_dict = {year: {"Total income": 0}}
            for month in month_list:
                income_record_dict[year][month] = 0
            income_doc.set(income_record_dict)
        # default income list document
        incomeItem_ref.set(incomeItem_dict)

        expenseItem_dict = {}
        for expense_item in default_expenseItem_list:
            expenseItem_dict[expense_item] = expense_item
            # 建立default expense document，給後續記帳record使用
            expense_doc = db.collection(user_email).document("Record").collection("expenseItem").document(expense_item)
            expense_record_dict = {year: {"Total expense": 0}}
            for month in month_list:
                expense_record_dict[year][month] = 0
            expense_doc.set(expense_record_dict)
        # default expense list document
        expenseItem_ref.set(expenseItem_dict)

        return default_incomeItem_list, default_expenseItem_list

    ## income item尚未儲存, expense item已儲存 ##
    elif not incomeItem_dict and expenseItem_dict:
        incomeItem_dict = {}
        for income_item in default_incomeItem_list:
            incomeItem_dict[income_item] = income_item
            # 建立default income document，給後續記帳record使用
            income_doc = db.collection(user_email).document("Record").collection("incomeItem").document(income_item)
            income_record_dict = {year: {"Total income": 0}}
            for month in month_list:
                income_record_dict[year][month] = 0
            income_doc.set(income_record_dict)
        incomeItem_ref.set(incomeItem_dict) 

        expenseItem_list = []
        for key, item in expenseItem_dict.items():
            # 注意：若遇到更改年份時，需要update新年份dict到firebase中
            expense_doc = db.collection(user_email).document("Record").collection("expenseItem").document(key)
            expense_record_dict = expense_doc.get().to_dict()
            if year not in expense_record_dict:
                expense_record_dict = {year: {"Total expense": 0}}
                for month in month_list:
                    expense_record_dict[year][month] = 0 
                expense_doc.update(expense_record_dict) 
            # 蒐集list內容
            expenseItem_list.append(item)
        sorted_expenseItem_list = sorted(expenseItem_list)

        return default_incomeItem_list, sorted_expenseItem_list
    
    ## income item已儲存, expense item尚未儲存 ##
    elif incomeItem_dict and not expenseItem_dict:
        incomeItem_list = []
        for key, item in incomeItem_dict.items():
            # 注意：若遇到更改年份時，需要update新年份dict到firebase中
            income_doc = db.collection(user_email).document("Record").collection("incomeItem").document(key)
            income_record_dict = income_doc.get().to_dict()
            if year not in income_record_dict:
                income_record_dict = {year: {"Total income": 0}}
                for month in month_list:
                    income_record_dict[year][month] = 0 
                income_doc.update(income_record_dict) 
            # 蒐集list內容
            incomeItem_list.append(item) 
        sorted_incomeItem_list = sorted(incomeItem_list)

        expenseItem_dict = {}
        for expense_item in default_expenseItem_list:
            expenseItem_dict[expense_item] = expense_item
            # 建立default expense document，給後續記帳record使用
            expense_doc = db.collection(user_email).document("Record").collection("expenseItem").document(expense_item)
            expense_record_dict = {year: {"Total expense": 0}}
            for month in month_list:
                expense_record_dict[year][month] = 0
            expense_doc.set(expense_record_dict)
        expenseItem_ref.set(expenseItem_dict)
        
        return sorted_incomeItem_list, default_expenseItem_list

    ## income item, expense item皆已儲存 ##
    elif incomeItem_dict and expenseItem_dict:
        incomeItem_list = []
        for key, item in incomeItem_dict.items():
            # 注意：若遇到更改年份時，需要update新年份dict到firebase中
            income_doc = db.collection(user_email).document("Record").collection("incomeItem").document(key)
            income_record_dict = income_doc.get().to_dict()
            if year not in income_record_dict:
                income_record_dict = {year: {"Total income": 0}}
                for month in month_list:
                    income_record_dict[year][month] = 0 
                income_doc.update(income_record_dict) 
            # 蒐集list內容
            incomeItem_list.append(item) 
        sorted_incomeItem_list = sorted(incomeItem_list)

        expenseItem_list = []
        for key, item in expenseItem_dict.items():
            # 注意：若遇到更改年份時，需要update新年份dict到firebase中
            expense_doc = db.collection(user_email).document("Record").collection("expenseItem").document(key)
            expense_record_dict = expense_doc.get().to_dict()
            if year not in expense_record_dict:
                expense_record_dict = {year: {"Total expense": 0}}
                for month in month_list:
                    expense_record_dict[year][month] = 0 
                expense_doc.update(expense_record_dict) 
            # 蒐集list內容
            expenseItem_list.append(item)
        sorted_expenseItem_list = sorted(expenseItem_list)

        return sorted_incomeItem_list, sorted_expenseItem_list

# modify list from user's modification
def modify_list(form_type, delete_list, add_list, year, user_email):
    year = str(year)
    month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    if form_type == "settingAccountDataForm":
        account_ref = db.collection(user_email).document("Record").collection("yourAccount").document("list")
        account_dict = account_ref.get().to_dict()

        for key, value in delete_list.items():
            del account_dict[key]
            # delete account document (Notice this step, the data will be eliminated permanently)
            delete_ref = db.collection(user_email).document("Record").collection("yourAccount").document(key)
            delete_ref.delete() 
        for key, value in add_list.items():
            account_dict[key] = value
            # add account document
            add_ref = db.collection(user_email).document("Record").collection("yourAccount").document(key)
            add_dict = {year: {"Account balance": 0}}
            for month in month_list:
                add_dict[year][month] = 0
            add_ref.set(add_dict)
        # update account list
        account_ref.set(account_dict)
        
    elif form_type == "settingIncomeDataForm":
        incomeItem_ref = db.collection(user_email).document("Record").collection("incomeItem").document("list")
        incomeItem_dict = incomeItem_ref.get().to_dict()

        for key, value in delete_list.items():
            del incomeItem_dict[key]
            # delete incomeItem document (Notice this step, the data will be eliminated permanently)
            delete_ref = db.collection(user_email).document("Record").collection("incomeItem").document(key)
            delete_ref.delete() 
        for key, value in add_list.items():
            incomeItem_dict[key] = value
            # add incomeItem document
            add_ref = db.collection(user_email).document("Record").collection("incomeItem").document(key)
            add_dict = {year: {"Total income": 0}}
            for month in month_list:
                add_dict[year][month] = 0
            add_ref.set(add_dict)
        # update incomeItem list
        incomeItem_ref.set(incomeItem_dict)
    
    elif form_type == "settingExpenseDataForm":
        expenseItem_ref = db.collection(user_email).document("Record").collection("expenseItem").document("list")
        expenseItem_dict = expenseItem_ref.get().to_dict()

        for key, value in delete_list.items():
            del expenseItem_dict[key]
            # delete expenseItem document (Notice this step, the data will be eliminated permanently)
            delete_ref = db.collection(user_email).document("Record").collection("expenseItem").document(key)
            delete_ref.delete()
        for key, value in add_list.items():
            expenseItem_dict[key] = value
            # add expenseItem document
            add_ref = db.collection(user_email).document("Record").collection("expenseItem").document(key)
            add_dict = {year: {"Total expense": 0}}
            for month in month_list:
                add_dict[year][month] = 0
            add_ref.set(add_dict)
        # update expenseItem list
        expenseItem_ref.set(expenseItem_dict)


