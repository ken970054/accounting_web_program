//Why can not declare global const here?

$(document).ready(function() {
    
    // read edit item's date and time and input to editItem_modal
    $("#todayTable, #yesterdayTable").on('click','.editButton',function() {
        // get the current row
        var currentRow = $(this).closest("tr"); 
        
        var record_type = currentRow.find("th").text(); // get type data
        var recordTypeArr = record_type.split(" ");
        var transType = recordTypeArr[0];
        recordCount_edit = recordTypeArr[1];
        
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
        var income_input = document.getElementById("editIncomeTypeInput");
        var expend_input = document.getElementById("editExpendTypeInput");
        var trans_input = document.getElementById("editTransTypeInput");
        
        $("#editTransType").html(transType);
        document.querySelector('#editMonth [value="' + record_month + '"]').selected = true; // make selector show record_month data

        if (transType === "Income"){
            income_input.style.display = 'flex';
            expend_input.style.display = 'none';
            trans_input.style.display = 'none';
            
            // show original data
            document.querySelector('#editIncomeItem [value="' + record_item + '"]').selected = true; 
            document.getElementById("editInputMoney").value = record_money; 
            document.querySelector('#editIncomeAccount [value="' + record_incomeAccount + '"]').selected = true;
            document.getElementById("editIncomeNote").value = record_note; 

            document.querySelector('#editInputMoney').onkeyup = function() {
                var inputMoney = document.querySelector('#editInputMoney').value;
                if (inputMoney === "") {
                    document.querySelector('#editSubmitRecord').disabled = true;
                    document.getElementById("editInputMoney_message").innerHTML = "Please enter input money.";
                }
                else {
                    document.querySelector('#editSubmitRecord').disabled = false; 
                    document.getElementById("editInputMoney_message").innerHTML = "";
                }
            }
            
        }
        else if (transType === "Expense"){
            income_input.style.display = 'none';
            expend_input.style.display = 'flex';
            trans_input.style.display = 'none';

            // show original data
            document.querySelector('#editExpendItem [value="' + record_item + '"]').selected = true;
            document.getElementById("editCostMoney").value = record_money; 
            document.querySelector('#editExpendAccount [value="' + record_expendAccount + '"]').selected = true;
            document.getElementById("editExpendNote").value = record_note; 

            document.querySelector('#editCostMoney').onkeyup = function() {
                var costMoney = document.querySelector('#editCostMoney').value;
                if (costMoney === "") {
                    document.querySelector('#editSubmitRecord').disabled = true;
                    document.getElementById("editCostMoney_message").innerHTML = "Please enter cost money.";
                }
                else {
                    document.querySelector('#editSubmitRecord').disabled = false; 
                    document.getElementById("editCostMoney_message").innerHTML = "";
                }
            }
        }
        else if (transType === "Transfer"){
            income_input.style.display = 'none';
            expend_input.style.display = 'none';
            trans_input.style.display = 'flex';

            // show original data
            document.querySelector('#editWithdrawAccount [value="' + record_expendAccount + '"]').selected = true;
            document.getElementById("editTransAmount").value = record_money; 
            document.querySelector('#editDepositAccount [value="' + record_incomeAccount + '"]').selected = true;
            document.getElementById("editTransNote").value = record_note; 

            document.querySelector('#editTransAmount').onkeyup = function() {
                var costMoney = document.querySelector('#editTransAmount').value;
                if (costMoney === "") {
                    document.querySelector('#editSubmitRecord').disabled = true;
                    document.getElementById("editTransAmount_message").innerHTML = "Please enter transfer money.";
                }
                else {
                    document.querySelector('#editSubmitRecord').disabled = false; 
                    document.getElementById("editTransAmount_message").innerHTML = "";
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
function disableEditButton(btn) {
    document.getElementById('editSubmitRecord').disabled = true;
}


// Pass edit data to backend
$('#editDataForm').submit(function (event) {
    event.preventDefault(); // 避免畫面重新整理
    
    //var transType = $('#inputTransType').val();
    var transType = document.getElementById("editTransType").innerHTML;
    if (transType === "Income"){
        const form =  {
            editButton: true,
            transactionType: transType,
            month: $('#editMonth').val(),
            incomeItem: $('#editIncomeItem').val(),
            amountOfMoney: $('#editInputMoney').val(),
            incomeAccount: $('#editIncomeAccount').val(),
            incomeNote: $('#editIncomeNote').val(),
            recordCount: recordCount_edit,
            recordDate: datetimeArr_edit[0],
            recordTime: datetimeArr_edit[1]
        };
        const path = '/';
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
            editButton: true,
            transactionType: transType,
            month: $('#editMonth').val(),
            expendItem: $('#editExpendItem').val(),
            amountOfMoney: $('#editCostMoney').val(),
            expendAccount: $('#editExpendAccount').val(),
            expendNote: $('#editExpendNote').val(),
            recordCount: recordCount_edit,
            recordDate: datetimeArr_edit[0],
            recordTime: datetimeArr_edit[1]
        };
        const path = '/';
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
            editButton: true,
            transactionType: transType,
            month: $('#editMonth').val(),
            withdrawAccount: $('#editWithdrawAccount').val(),
            transAmount: $('#editTransAmount').val(),
            depositAccount: $('#editDepositAccount').val(),
            transNote: $('#editTransNote').val(),
            recordCount: recordCount_edit,
            recordDate: datetimeArr_edit[0],
            recordTime: datetimeArr_edit[1]
        };
        const path = '/';
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