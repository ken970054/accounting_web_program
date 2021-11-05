from firebase_admin import firestore

import time

from flask.helpers import total_seconds

db = firestore.client()

#### get monthly detail in each account ####
def get_account_detail(account_list, selected_year, user_email):
    selected_year = str(selected_year)
    all_accountDict = {}
    for account in account_list:
        account_ref = db.collection(user_email).document("Record").collection("yourAccount").document(account)
        account_dict = account_ref.get().to_dict()
        for year, account_detail in account_dict.items():
            if selected_year == year:
                all_accountDict[account] = account_detail
    return all_accountDict

#### get monthly detail in each income item ####
def get_income_detail(income_list, selected_year, user_email):
    selected_year = str(selected_year)
    all_incomeDict = {}
    for incomeItem in income_list:
        income_ref = db.collection(user_email).document("Record").collection("incomeItem").document(incomeItem)
        income_dict = income_ref.get().to_dict()
        for year, income_detail in income_dict.items():
            if selected_year == year:
                all_incomeDict[incomeItem] = income_detail
    return all_incomeDict 

#### get monthly detail in each expense item ####
def get_expense_detail(expense_list, selected_year, user_email):
    selected_year = str(selected_year)
    all_expenseDict = {}
    for expenseItem in expense_list:
        expense_ref = db.collection(user_email).document("Record").collection("expenseItem").document(expenseItem)
        expense_dict = expense_ref.get().to_dict()
        for year, expense_detail in expense_dict.items():
            if selected_year == year:
                all_expenseDict[expenseItem] = expense_detail
    return all_expenseDict 


def calculateTableContent(selected_account_name, originalDeposit, selected_year, Account, user_email):
    # If there is no record yet, does that mattre to this function?

    ## calculate total income in each account for account balance and gross income table ##
    income_ref = db.collection(user_email).document("Record").collection("Income").document("YY" + selected_year).collections()
    total_income_dict = {}
    item_income_dict = {}
    # processing total income in each account and each month
    for months_record in income_ref:
        for days_record in months_record.stream():
            days_dict = days_record.to_dict()
            current_account = days_dict['incomeAccount']
            current_item = days_dict['incomeItem']
            current_month = days_dict['month']
            # need to change to int because of the calculation
            current_money = int(days_dict['money'])

            ## deal with incomeAccount
            # if there is no such account for this day record, initialize it by its month and money
            if  current_account not in total_income_dict:
                total_income_dict[current_account] = { current_month: current_money }
            else:
                # if there is no such month in this account, assign its month and money to it
                if current_month not in total_income_dict[current_account]:
                    total_income_dict[current_account][current_month] = current_money
                else:
                    total_income_dict[current_account][current_month] = total_income_dict[current_account][current_month] + current_money
            ## deal with incomeItem
            if  current_item not in item_income_dict:
                item_income_dict[current_item] = { current_month: current_money }
            else:
                if current_month not in item_income_dict[current_item]:
                    item_income_dict[current_item][current_month] = current_money
                else:
                    item_income_dict[current_item][current_month] = item_income_dict[current_item][current_month] + current_money
    #print(f"income: {total_income_dict}")
                    

    ## calculate total expense in each account for account balance and total expense table ##
    expense_ref = db.collection(user_email).document("Record").collection("Expense").document("YY" + selected_year).collections()
    total_expense_dict = {}
    item_expense_dict = {}
    # processing total expense in each account and each month
    for months_record in expense_ref:
        for days_record in months_record.stream():
            days_dict = days_record.to_dict()
            current_account = days_dict['expendAccount']
            current_item = days_dict['expendItem']
            current_month = days_dict['month']
            # need to change to int because of the calculation
            current_money = int(days_dict['money'])

            ## deal with expenseAccount
            # if there is no such account for this day record, initialize it by its month and money
            if  current_account not in total_expense_dict:
                total_expense_dict[current_account] = { current_month: current_money }
            else:
                # if there is no such month in this account, assign its month and money to it
                if current_month not in total_expense_dict[current_account]:
                    total_expense_dict[current_account][current_month] = current_money
                else:
                    total_expense_dict[current_account][current_month] = total_expense_dict[current_account][current_month] + current_money
            
            ## deal with expenseItem
            if  current_item not in item_expense_dict:
                item_expense_dict[current_item] = { current_month: current_money }
            else:
                # if there is no such month in this account, assign its month and money to it
                if current_month not in item_expense_dict[current_item]:
                    item_expense_dict[current_item][current_month] = current_money
                else:
                    item_expense_dict[current_item][current_month] = item_expense_dict[current_item][current_month] + current_money
    #print(f"expense: {total_expense_dict}")
    
    
    ## calculate total transfer in and transfer out in each account for account balance only##
    transfer_ref = db.collection(user_email).document("Record").collection("Transfer").document("YY" + selected_year).collections()
    total_transferIn_dict = {}
    total_transferOut_dict = {}
    for months_record in transfer_ref:
        for days_record in months_record.stream():
            days_dict = days_record.to_dict()
            depositAccount = days_dict['depositAccount']
            withdrawAccount = days_dict['withdrawAccount']
            # need to change to int because of the calculation
            current_money = int(days_dict['transAmount'])
            # if account name not in transfer in or transfer out, initialize it. Otherwise, add money to it
            if depositAccount not in total_transferIn_dict and withdrawAccount not in total_transferOut_dict:
                total_transferIn_dict[depositAccount] = current_money
                total_transferOut_dict[withdrawAccount] = current_money
            elif depositAccount not in total_transferIn_dict and withdrawAccount in total_transferOut_dict:
                total_transferIn_dict[depositAccount] = current_money
                total_transferOut_dict[withdrawAccount] = total_transferOut_dict[withdrawAccount] + current_money
            elif depositAccount in total_transferIn_dict and withdrawAccount not in total_transferOut_dict:
                total_transferIn_dict[depositAccount] = total_transferIn_dict[depositAccount] + current_money
                total_transferOut_dict[withdrawAccount] = current_money
            else:
                total_transferIn_dict[depositAccount] = total_transferIn_dict[depositAccount] + current_money
                total_transferOut_dict[withdrawAccount] = total_transferOut_dict[withdrawAccount] + current_money
    #print(f"transfer in: {total_transferIn_dict}")
    #print(f"transfer out: {total_transferOut_dict}")

    
    #### deal with account balance table in each account
    for account_name in Account:
        account_balance_ref = db.collection(user_email).document("Record").collection("yourAccount").document(account_name)
        account_balance_dict = account_balance_ref.get().to_dict()

        # update account original deposit in dict if it matches to selected account
        if account_name == selected_account_name:
            account_balance_dict[selected_year]["Original deposit"] = int(originalDeposit)

        ## calculate certain account balance = original deposit + income + transfer in - expense - transfer out
        # + income
        total_income = 0
        if account_name in total_income_dict:
            for month, money  in total_income_dict[account_name].items():
                total_income = total_income + money
        # + transfer in
        total_transferIn = 0
        if account_name in total_transferIn_dict:
            total_transferIn = total_transferIn_dict[account_name]
        # - expense
        total_expense = 0
        if account_name in total_expense_dict:
            for month, money  in total_expense_dict[account_name].items():
                total_expense = total_expense + money
                # modify account expense as well
                account_balance_dict[selected_year][month] = money
        # - transfer out
        total_transferOut = 0
        if account_name in total_transferOut_dict:
            total_transferOut = total_transferOut_dict[account_name]
            
        # update account balance in dict
        account_balance_dict[selected_year]["Account balance"] = account_balance_dict[selected_year]["Original deposit"] + total_income + total_transferIn - total_expense - total_transferOut

        # update dict to firebase doc
        account_balance_ref.update(account_balance_dict)
    
    #### deal with gross income table
    for item_name, month_dict in item_income_dict.items():
        incomeItem_ref = db.collection(user_email).document("Record").collection("incomeItem").document(item_name)
        incomeItem_dict = incomeItem_ref.get().to_dict()
        total_income = 0
        for month, money in month_dict.items():
            incomeItem_dict[selected_year][month] = money
            total_income = total_income + money

        incomeItem_dict[selected_year]['Total income'] = total_income
        incomeItem_ref.update(incomeItem_dict)

    #### deal with expense table
    for item_name, month_dict in item_expense_dict.items():
        expenseItem_ref = db.collection(user_email).document("Record").collection("expenseItem").document(item_name)
        expenseItem_dict = expenseItem_ref.get().to_dict()
        total_expense = 0
        for month, money in month_dict.items():
            expenseItem_dict[selected_year][month] = money
            total_expense = total_expense + money

        expenseItem_dict[selected_year]['Total expense'] = total_expense
        expenseItem_ref.update(expenseItem_dict)

def digitComma(value):
    return f"{value:,}"