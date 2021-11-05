
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
            if not account_dict:
                account_dict[year] = {account: account}
            else:
                account_dict[year][account] = account
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
        # 若遇到新的一年第一筆紀錄，將去年的list內容複製到新一年的list
        if year not in account_dict:
            account_dict[year] = account_dict[last_year]
            for key, account in account_dict[year].items():
                account_list.append(account)
        else:
            for key, account in account_dict[year].items():
                # 注意：若遇到更改年份時，需要update新年份dict到firebase中，且account要沿用先前的balance值
                account_doc = db.collection(user_email).document("Record").collection("yourAccount").document(account)
                account_record_dict = account_doc.get().to_dict()
                if year not in account_record_dict:
                    last_year_balance = account_record_dict[last_year]["Account balance"]
                    account_record_dict[year]["Account balance"] = last_year_balance
                    account_record_dict[year]["Original deposit"] = last_year_balance
                    for month in month_list:
                        account_record_dict[year][month] = 0 
                    account_doc.update(account_record_dict)
                
                # 蒐集list內容
                account_list.append(account)
        
        sorted_account_list = sorted(account_list)
        return sorted_account_list
            


# get income and expense items list or set default for html use
def get_items_list(year, user_email):
    last_year = year - 1
    last_year = str(last_year)
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
            if not incomeItem_dict:
                incomeItem_dict[year] = {income_item: income_item}
            else:
                incomeItem_dict[year][income_item] = income_item
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
            if not expenseItem_dict:
                expenseItem_dict[year] = {expense_item: expense_item}
            else:
                expenseItem_dict[year][expense_item] = expense_item
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
            if not incomeItem_dict:
                incomeItem_dict[year] = {income_item: income_item}
            else:
                incomeItem_dict[year][income_item] = income_item
            # 建立default income document，給後續記帳record使用
            income_doc = db.collection(user_email).document("Record").collection("incomeItem").document(income_item)
            income_record_dict = {year: {"Total income": 0}}
            for month in month_list:
                income_record_dict[year][month] = 0
            income_doc.set(income_record_dict)
        incomeItem_ref.set(incomeItem_dict) 

        expenseItem_list = []
        # 若遇到新的一年第一筆紀錄，將去年的list內容複製到新一年的list
        if year not in expenseItem_dict:
            expenseItem_dict[year] = expenseItem_dict[last_year]
            for key, expenseItem in expenseItem_dict[year].items():
                expenseItem_list.append(expenseItem)
        else:
            for key, item in expenseItem_dict[year].items():
                # 注意：若遇到更改年份時，需要update新年份dict到firebase中
                expense_doc = db.collection(user_email).document("Record").collection("expenseItem").document(item)
                expense_record_dict = expense_doc.get().to_dict()
                if year not in expense_record_dict:
                    expense_record_dict[year]["Total expense"] = 0
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
        # 若遇到新的一年第一筆紀錄，將去年的list內容複製到新一年的list
        if year not in incomeItem_dict:
            incomeItem_dict[year] = incomeItem_dict[last_year]
            for key, incomeItem in incomeItem_dict[year].items():
                incomeItem_list.append(incomeItem)
        else:
            for key, item in incomeItem_dict[year].items():
                # 注意：若遇到更改年份時，需要update新年份dict到firebase中
                income_doc = db.collection(user_email).document("Record").collection("incomeItem").document(item)
                income_record_dict = income_doc.get().to_dict()
                if year not in income_record_dict:
                    income_record_dict[year]["Total income"] = 0
                    for month in month_list:
                        income_record_dict[year][month] = 0 
                    income_doc.update(income_record_dict) 
                # 蒐集list內容
                incomeItem_list.append(item) 
        sorted_incomeItem_list = sorted(incomeItem_list)

        expenseItem_dict = {}
        for expense_item in default_expenseItem_list:
            if not expenseItem_dict:
                expenseItem_dict[year] = {expense_item: expense_item}
            else:
                expenseItem_dict[year][expense_item] = expense_item
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
        # 若遇到新的一年第一筆紀錄，將去年的list內容複製到新一年的list
        if year not in incomeItem_dict:
            incomeItem_dict[year] = incomeItem_dict[last_year]
            for key, incomeItem in incomeItem_dict[year].items():
                incomeItem_list.append(incomeItem)
        else:
            for key, item in incomeItem_dict[year].items():
                # 注意：若遇到更改年份時，需要update新年份dict到firebase中
                income_doc = db.collection(user_email).document("Record").collection("incomeItem").document(item)
                income_record_dict = income_doc.get().to_dict()
                if year not in income_record_dict:
                    income_record_dict[year]["Total income"] = 0
                    for month in month_list:
                        income_record_dict[year][month] = 0 
                    income_doc.update(income_record_dict)
                # 蒐集list內容
                incomeItem_list.append(item) 
        sorted_incomeItem_list = sorted(incomeItem_list)

        expenseItem_list = []
        # 若遇到新的一年第一筆紀錄，將去年的list內容複製到新一年的list
        if year not in expenseItem_dict:
            expenseItem_dict[year] = expenseItem_dict[last_year]
            for key, expenseItem in expenseItem_dict[year].items():
                expenseItem_list.append(expenseItem)
        else:
            for key, item in expenseItem_dict[year].items():
                # 注意：若遇到更改年份時，需要update新年份dict到firebase中
                expense_doc = db.collection(user_email).document("Record").collection("expenseItem").document(item)
                expense_record_dict = expense_doc.get().to_dict()
                if year not in expense_record_dict:
                    expense_record_dict[year]["Total expense"] = 0
                    for month in month_list:
                        expense_record_dict[year][month] = 0 
                    expense_doc.update(expense_record_dict) 
                # 蒐集list內容
                expenseItem_list.append(item)
        sorted_expenseItem_list = sorted(expenseItem_list)

        return sorted_incomeItem_list, sorted_expenseItem_list

#### modify list from user's modification
def modify_list(form_type, delete_list, add_list, year, user_email):
    year = str(year)
    month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    if form_type == "settingAccountDataForm":
        account_list_ref = db.collection(user_email).document("Record").collection("yourAccount").document("list")
        account_list_dict = account_list_ref.get().to_dict()

        for deleted_account, value in delete_list.items():
            ## only delete the related materials in that year, which means you cannot delete the accounts or items in the past
            # delete list content in that year
            del account_list_dict[year][deleted_account]
            # delete account document (Notice this step, the data will be eliminated permanently)
            delete_account_ref = db.collection(user_email).document("Record").collection("yourAccount").document(deleted_account)
            delete_account_dict = delete_account_ref.get().to_dict()
            if len(delete_account_dict) == 1:
                delete_account_ref.delete() 
            else:
                del delete_account_dict[year]
            
            ## delete all record related to this account
            # income part
            income_ref = db.collection(user_email).document("Record").collection("Income").document("YY" + year).collections()
            for months_record in income_ref:
                for days_record in months_record.stream():
                    days_dict = days_record.to_dict()
                    record_account = days_dict['incomeAccount']
                    record_month = days_dict['month']
                    record_item = days_dict['incomeItem']
                    record_money = int(days_dict['money'])
                    # substract money to the record where incomeItem fit the record_month and record_item to correct the gross income table, then delete this record
                    if deleted_account == record_account:
                        incomeItem_ref = db.collection(user_email).document("Record").collection("incomeItem").document(record_item)
                        incomeItem_dict = incomeItem_ref.get().to_dict()
                        incomeItem_dict[year][record_month] = incomeItem_dict[year][record_month] - record_money
                        incomeItem_dict[year]['Total income'] = incomeItem_dict[year]['Total income'] - record_money
                        incomeItem_ref.update(incomeItem_dict)
                        days_record.reference.delete()
            # expense part
            expense_ref = db.collection(user_email).document("Record").collection("Expense").document("YY" + year).collections()
            for months_record in expense_ref:
                for days_record in months_record.stream():
                    days_dict = days_record.to_dict()
                    record_account = days_dict['expendAccount']
                    record_month = days_dict['month']
                    record_item = days_dict['expendItem']
                    record_money = int(days_dict['money'])
                    # add money back to the record where incomeItem fit the record_month and record_item to correct the gross income table, then delete this record
                    if deleted_account == record_account:
                        expenseItem_ref = db.collection(user_email).document("Record").collection("expenseItem").document(record_item)
                        expenseItem_dict = expenseItem_ref.get().to_dict()
                        expenseItem_dict[year][record_month] = expenseItem_dict[year][record_month] + record_money
                        expenseItem_dict[year]['Total expense'] = expenseItem_dict[year]['Total expense'] + record_money
                        expenseItem_ref.update(expenseItem_dict)
                        days_record.reference.delete()
            # transfer part: 
            transfer_ref = db.collection(user_email).document("Record").collection("Transfer").document("YY" + year).collections()
            for months_record in transfer_ref:
                for days_record in months_record.stream():
                    days_dict = days_record.to_dict()
                    money = int(days_dict['transAmount'])
                    record_withdrawAccount = days_dict['withdrawAccount']
                    record_depositAccount = days_dict['depositAccount']
                    # if deleted account is withdrawAccount -> add money to original deposit in the depositAccount then delete the record
                    if deleted_account == record_withdrawAccount:
                        other_account_ref = db.collection(user_email).document("Record").collection("yourAccount").document(record_depositAccount)
                        other_account_dict = other_account_ref.get().to_dict()
                        other_account_dict[year]['Original deposit'] = other_account_dict[year]['Original deposit'] + money
                        other_account_ref.update(other_account_dict)
                        days_record.reference.delete()
                    # if deleted account is dspositAccount -> substract money to original deposit in the withdrawAccount then delete the record
                    if deleted_account == record_depositAccount:
                        other_account_ref = db.collection(user_email).document("Record").collection("yourAccount").document(record_withdrawAccount)
                        other_account_dict = other_account_ref.get().to_dict()
                        other_account_dict[year]['Original deposit'] = other_account_dict[year]['Original deposit'] - money
                        other_account_ref.update(other_account_dict)
                        days_record.reference.delete()

        ## add account part
        for added_account, value in add_list.items():
            account_list_dict[year][added_account] = value
            # add account document
            add_ref = db.collection(user_email).document("Record").collection("yourAccount").document(added_account)
            add_dict = add_ref.get().to_dict()
            if not add_dict:
                add_dict = {year: {"Account balance": 0, "Original deposit": 0}}
                for month in month_list:
                    add_dict[year][month] = 0
                add_ref.set(add_dict)
            else:
                add_dict[year]["Account balance"] = 0
                add_dict[year]["Original deposit"] = 0
                for month in month_list:
                    add_dict[year][month] = 0
                add_ref.update(add_dict)

        # update account list
        account_list_ref.set(account_list_dict)


    elif form_type == "settingIncomeDataForm":
        incomeItem_list_ref = db.collection(user_email).document("Record").collection("incomeItem").document("list")
        incomeItem_list_dict = incomeItem_list_ref.get().to_dict()

        for deleted_item, value in delete_list.items():
            # delete list content in that year
            del incomeItem_list_dict[year][deleted_item]
            # delete incomeItem document (Notice this step, the data will be eliminated permanently)
            delete_item_ref = db.collection(user_email).document("Record").collection("incomeItem").document(deleted_item)
            delete_item_dict = delete_item_ref.get().to_dict()
            if len(delete_item_dict) == 1:
                delete_item_ref.delete()
            else:
                del delete_item_dict[year]
            
            ## delete all record related to this income item
            income_ref = db.collection(user_email).document("Record").collection("Income").document("YY" + year).collections()
            for months_record in income_ref:
                for days_record in months_record.stream():
                    days_dict = days_record.to_dict()
                    record_item = days_dict['incomeItem']
                    record_account = days_dict['incomeAccount']
                    money = int(days_dict['money'])
                    if deleted_item == record_item:
                        # add money to the original deposit in this record's account to keep the balance correct
                        account_ref = db.collection(user_email).document("Record").collection("yourAccount").document(record_account)
                        account_dict = account_ref.get().to_dict()
                        account_dict[year]['Original deposit'] = account_dict[year]['Original deposit'] + money
                        account_ref.update(account_dict)
                        days_record.reference.delete()
                        

        for added_item, value in add_list.items():
            incomeItem_list_dict[year][added_item] = value
            # add incomeItem document
            add_ref = db.collection(user_email).document("Record").collection("incomeItem").document(added_item)
            add_dict = add_ref.get().to_dict()
            if not add_dict:
                add_dict = {year: {"Total income": 0}}
                for month in month_list:
                    add_dict[year][month] = 0
                add_ref.set(add_dict)
            else:
                add_dict[year]["Total income"] = 0
                for month in month_list:
                    add_dict[year][month] = 0
                add_ref.update(add_dict)
        # update incomeItem list
        incomeItem_list_ref.set(incomeItem_list_dict)
    
    elif form_type == "settingExpenseDataForm":
        expenseItem_list_ref = db.collection(user_email).document("Record").collection("expenseItem").document("list")
        expenseItem_list_dict = expenseItem_list_ref.get().to_dict()

        for deleted_item, value in delete_list.items():
            del expenseItem_list_dict[year][deleted_item]
            # delete expenseItem document (Notice this step, the data will be eliminated permanently)
            delete_item_ref = db.collection(user_email).document("Record").collection("expenseItem").document(deleted_item)
            delete_item_dict = delete_item_ref.get().to_dict()
            if len(delete_item_dict) == 1:
                delete_item_ref.delete()
            else:
                del delete_item_dict[year]
            
            ## delete all record related to this expense item
            expense_ref = db.collection(user_email).document("Record").collection("Expense").document("YY" + year).collections()
            for months_record in expense_ref:
                for days_record in months_record.stream():
                    days_dict = days_record.to_dict()
                    record_item = days_dict['expendItem']
                    record_account = days_dict['expendAccount']
                    money = int(days_dict['money'])
                    if deleted_item == record_item:
                        # subtract money to the original deposit in this record's account to keep the balance correct
                        account_ref = db.collection(user_email).document("Record").collection("yourAccount").document(record_account)
                        account_dict = account_ref.get().to_dict()
                        account_dict[year]['Original deposit'] = account_dict[year]['Original deposit'] - money
                        account_ref.update(account_dict)
                        days_record.reference.delete()
        
        for added_item, value in add_list.items():
            expenseItem_list_dict[year][added_item] = value
            # add expenseItem document
            add_ref = db.collection(user_email).document("Record").collection("expenseItem").document(added_item)
            add_dict = add_ref.get().to_dict()
            if not add_dict:
                add_dict = {year: {"Total income": 0}}
                for month in month_list:
                    add_dict[year][month] = 0
                add_ref.set(add_dict)
            else:
                add_dict[year]["Total income"] = 0
                for month in month_list:
                    add_dict[year][month] = 0
                add_ref.update(add_dict)
        # update expenseItem list
        expenseItem_list_ref.set(expenseItem_list_dict)


