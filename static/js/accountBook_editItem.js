//Why can not declare global const here?

$(document).ready(function() {
    
    // read edit item's date and time and input to editItem_modal
    $("#accountBook_table").on('click','.editButton',function() {
        // get the current row
        var currentRow = $(this).closest("tr"); 
        
        var record_type = currentRow.find("th").text(); // get type data
        var transType = record_type;
        recordCount_edit = currentRow.find("td:eq(9)").text();
        //console.log(recordCount_edit);
        
        var record_month = currentRow.find("td:eq(0)").text();
        var record_item = currentRow.find("td:eq(1)").text();
        
        var record_money = currentRow.find("td:eq(2)").text();
        // deal with the comma in the string
        record_money = record_money.replace(/,/g, "");

        var record_expendAccount = currentRow.find("td:eq(3)").text();
        var record_incomeAccount = currentRow.find("td:eq(4)").text();
        var record_note = currentRow.find("td:eq(5)").text();
        
        var record_datetime = currentRow.find("td:eq(6)").text(); // get timestamp data
        datetimeArr_edit = record_datetime.split(" "); // split date and time(no var means global variable)

        //// show different type of trans ////
        var income_input = document.getElementById("editIncomeTypeInput_book");
        var expend_input = document.getElementById("editExpendTypeInput_book");
        var trans_input = document.getElementById("editTransTypeInput_book");
        
        $("#editTransType_book").html(transType);
        document.querySelector('#editMonth_book [value="' + record_month + '"]').selected = true; // make selector show record_month data

        if (transType === "Income"){
            income_input.style.display = 'flex';
            expend_input.style.display = 'none';
            trans_input.style.display = 'none';
            
            // show original data
            document.querySelector('#editIncomeItem_book [value="' + record_item + '"]').selected = true; 
            document.getElementById("editInputMoney_book").value = record_money; 
            document.querySelector('#editIncomeAccount_book [value="' + record_incomeAccount + '"]').selected = true;
            document.getElementById("editIncomeNote_book").value = record_note; 

            document.querySelector('#editInputMoney_book').onkeyup = function() {
                var inputMoney = document.querySelector('#editInputMoney_book').value;
                if (inputMoney === "") {
                    document.querySelector('#editSubmitRecord_book').disabled = true;
                    document.getElementById("editInputMoney_message_book").innerHTML = "Please enter input money.";
                }
                else {
                    document.querySelector('#editSubmitRecord_book').disabled = false; 
                    document.getElementById("editInputMoney_message_book").innerHTML = "";
                }
            }
            
        }
        else if (transType === "Expense"){
            income_input.style.display = 'none';
            expend_input.style.display = 'flex';
            trans_input.style.display = 'none';

            // show original data
            document.querySelector('#editExpendItem_book [value="' + record_item + '"]').selected = true;
            document.getElementById("editCostMoney_book").value = record_money; 
            document.querySelector('#editExpendAccount_book [value="' + record_expendAccount + '"]').selected = true;
            document.getElementById("editExpendNote_book").value = record_note; 

            document.querySelector('#editCostMoney_book').onkeyup = function() {
                var costMoney = document.querySelector('#editCostMoney_book').value;
                if (costMoney === "") {
                    document.querySelector('#editSubmitRecord_book').disabled = true;
                    document.getElementById("editCostMoney_message_book").innerHTML = "Please enter cost money.";
                }
                else {
                    document.querySelector('#editSubmitRecord_book').disabled = false; 
                    document.getElementById("editCostMoney_message_book").innerHTML = "";
                }
            }
        }
        else if (transType === "Transfer"){
            income_input.style.display = 'none';
            expend_input.style.display = 'none';
            trans_input.style.display = 'flex';

            // show original data
            document.querySelector('#editWithdrawAccount_book [value="' + record_expendAccount + '"]').selected = true;
            document.getElementById("editTransAmount_book").value = record_money; 
            document.querySelector('#editDepositAccount_book [value="' + record_incomeAccount + '"]').selected = true;
            document.getElementById("editTransNote_book").value = record_note; 

            document.querySelector('#editTransAmount_book').onkeyup = function() {
                var costMoney = document.querySelector('#editTransAmount_book').value;
                if (costMoney === "") {
                    document.querySelector('#editSubmitRecord_book').disabled = true;
                    document.getElementById("editTransAmount_message_book").innerHTML = "Please enter transfer money.";
                }
                else {
                    document.querySelector('#editSubmitRecord_book').disabled = false; 
                    document.getElementById("editTransAmount_message_book").innerHTML = "";
                }
            }
        }
        else {
            income_input.style.display = 'none'; 
            expend_input.style.display = 'none';
            trans_input.style.display = 'none';
        }

        
    });
});


// Disabling the button after once click 
function disableEditButton_book(btn) {
    document.getElementById('editSubmitRecord_book').disabled = true;
}


// Pass edit data to backend
$('#editDataForm_book').submit(function (event) {
    event.preventDefault(); // 避免畫面重新整理
    
    //var transType = $('#inputTransType').val();
    var transType = document.getElementById("editTransType_book").innerHTML;
    if (transType === "Income"){
        const form =  {
            editButton_book: true,
            transactionType: transType,
            month: $('#editMonth_book').val(),
            incomeItem: $('#editIncomeItem_book').val(),
            amountOfMoney: $('#editInputMoney_book').val(),
            incomeAccount: $('#editIncomeAccount_book').val(),
            incomeNote: $('#editIncomeNote_book').val(),
            recordCount: recordCount_edit,
            recordDate: datetimeArr_edit[0],
            recordTime: datetimeArr_edit[1]
        };
        const path = '/account/book';
        axios.post(path, form, axiosConfig)
            .then(res => {
                console.log('[完成form傳遞]', form);
                window.location.reload();
            })
            .catch(err => {
                console.log('[傳遞form失敗]', err);
            });
    }
    else if (transType === "Expense"){
        const form =  {
            editButton_book: true,
            transactionType: transType,
            month: $('#editMonth_book').val(),
            expendItem: $('#editExpendItem_book').val(),
            amountOfMoney: $('#editCostMoney_book').val(),
            expendAccount: $('#editExpendAccount_book').val(),
            expendNote: $('#editExpendNote_book').val(),
            recordCount: recordCount_edit,
            recordDate: datetimeArr_edit[0],
            recordTime: datetimeArr_edit[1]
        };
        const path = '/account/book';
        axios.post(path, form, axiosConfig)
            .then(res => {
                console.log('[完成form傳遞]', form);
                window.location.reload();
            })
            .catch(err => {
                console.log('[傳遞form失敗]', err);
            });

    }
    else if (transType === "Transfer"){
        const form =  {
            editButton_book: true,
            transactionType: transType,
            month: $('#editMonth_book').val(),
            withdrawAccount: $('#editWithdrawAccount_book').val(),
            transAmount: $('#editTransAmount_book').val(),
            depositAccount: $('#editDepositAccount_book').val(),
            transNote: $('#editTransNote_book').val(),
            recordCount: recordCount_edit,
            recordDate: datetimeArr_edit[0],
            recordTime: datetimeArr_edit[1]
        };
        const path = '/account/book';
        axios.post(path, form, axiosConfig)
            .then(res => {
                console.log('[完成form傳遞]', form);
                window.location.reload();
            })
            .catch(err => {
                console.log('[傳遞form失敗]', err);
            });

    }
});