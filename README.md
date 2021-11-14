# CO$T $AVING
Video Demo:  https://youtu.be/_gPpEOTnzLo

Website Link built on Heroku: https://accounting-web-program.herokuapp.com/

(You can use account: test03@gmail.com, password: 123456 to login and demo)

> An app to take your daily financial records.



# Files Description
In the project directory, you can run:
#### `python app.py`
Run the app in the development mode.
Open http://0.0.0.0:5000/ to view in your browser.

## Main pages
#### Front-end
General layout for all the pages: layout.html, style.css
1. `Home`
   - User login or sign up
   - Button for adding one new record and show records in two days from now
   - **Include files**
     - HTML: index.html, login_modal.html, sign_up_modal.html, newItem_modal.html, editItem_modal.html
     - JavaScript: main.js, newItem.js, editItem.js
2. `Account Book`
   - Take 1~5 records at a time
   - Show history monthly record table by user selecting
   - **Include files**
     - HTML: account_book.html, editItem_modal.html, 
     - JavaScript: accountBook.js, accountBook_editItem.js, accountBook_deleteItem.js
3. `Account Management`
   - Organize your account balance, gross income and expense record each year
   - User can modify the account original deposit if any
   - **Include files**
     - HTML: account_manage.html, accountDepositEdit_modal.html, 
     - JavaScript: accountManage_edit.js
4. `Setting`
   - Set the category of user's account, income item and expense item (There will be default item)
   - **Include files**
     - HTML: setting.html, settingEdit_modal.html, 
     - JavaScript: setting_editItem.js

#### Back-end
* Main function: app.py
  - Control all routes in different pages
  - Set up environment for Flask and Firebase
  - Get data from Firebase and send to .html pages
* Function for get records for html: recordFunctions.py
* Function for setting categories: settingFunction.py 
* Function for calculating the account balance and income, expense of items: calculateFunction.py

#### Implement framework and tools
* Flask, AJAX, jQuery
* Heroku, Firebase
