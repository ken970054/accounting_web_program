//Why can not declare global const here?

$(document).ready(function() {
    
    // add, remove new record item
    $('#record_add').on('click', add);
    $('#record_remove').on('click', remove);

    function add(event) {
        event.preventDefault(); // 避免畫面重新整理
        var new_record_no = parseInt($('#total_record').val()) + 1;
        var new_record_item = document.getElementById('recordGroup_1').innerHTML;
        var add_item = "<div class='form-row justify-content-center rounded-pill' id='recordGroup_" + new_record_no +"' style='border-width:3px; border-style:solid; border-color:#D3D3D3; margin:15px'>\n " + new_record_item +" \n</div>" 
        
        if (new_record_no < 6) {
            //alert(new_record_item);
            $('#record_block').append(add_item);
            $('#total_record').val(new_record_no);
        }
        else {
            alert("Too many record!!");
        }
    }

    function remove(event) {
        event.preventDefault(); // 避免畫面重新整理
        var last_record_no = $('#total_record').val();
        if (last_record_no > 1) {
            $('#recordGroup_' + last_record_no).remove();
            $('#total_record').val(last_record_no - 1);
        }
    }


    // showing the form of selecting trans type (separate different record implementation)
    $('#recordGroup_1').find('#inputTransType_book').on('change', show_transType_account);

    function show_transType_account() {
        var transType = this.value;
        var selectID = this.id;
        var typeInputID = $(selectID).parent().childern('')
        var income_input = document.getElementById("incomeTypeInput_book");
        //var income_input = document.getElementById(transId);
        var expend_input = document.getElementById("expendTypeInput_book");
        var trans_input = document.getElementById("transTypeInput_book");
        
    
        if (transType === "Income"){
            income_input.style.display = 'flex';
            expend_input.style.display = 'none';
            trans_input.style.display = 'none';
    }



});

// showing the form of selecting trans type
function show_transType_account_temp(v)
{
    //var transType = v;
    var transType = v.value;
    var parent = v.id;
    var income_input = document.getElementById("incomeTypeInput_book");
    //var income_input = document.getElementById(transId);
    var expend_input = document.getElementById("expendTypeInput_book");
    var trans_input = document.getElementById("transTypeInput_book");
    

    if (transType === "Income"){
        income_input.style.display = 'flex';
        expend_input.style.display = 'none';
        trans_input.style.display = 'none';

        document.querySelector('#inputMoney_book').onkeyup = function() {
            var inputMoney = document.querySelector('#inputMoney_book').value;
            if (inputMoney === "") {
                document.querySelector('#submitRecord_book').disabled = true;
                document.getElementById("inputMoney_message_book").innerHTML = "Please enter input money.";
            }
            else {
                document.querySelector('#submitRecord_book').disabled = false; 
                document.getElementById("inputMoney_message_book").innerHTML = "";
            }
        }
    }
    else if (transType === "Expense"){
        income_input.style.display = 'none';
        expend_input.style.display = 'flex';
        trans_input.style.display = 'none';

        document.querySelector('#costMoney_book').onkeyup = function() {
            var costMoney = document.querySelector('#costMoney_book').value;
            if (costMoney === "") {
                document.querySelector('#submitRecord_book').disabled = true;
                document.getElementById("costMoney_message_book").innerHTML = "Please enter cost money.";
            }
            else {
                document.querySelector('#submitRecord_book').disabled = false; 
                document.getElementById("costMoney_message_book").innerHTML = "";
            }
        }
    }
    else if (transType === "Transfer"){
        income_input.style.display = 'none';
        expend_input.style.display = 'none';
        trans_input.style.display = 'flex';

        document.querySelector('#transAmount_book').onkeyup = function() {
            var costMoney = document.querySelector('#transAmount_book').value;
            if (costMoney === "") {
                document.querySelector('#submitRecord_book').disabled = true;
                document.getElementById("transAmount_message_book").innerHTML = "Please enter transfer money.";
            }
            else {
                document.querySelector('#submitRecord_book').disabled = false; 
                document.getElementById("transAmount_message_book").innerHTML = "";
            }
        }
    }
    else {
        income_input.style.display = 'none'; 
        expend_input.style.display = 'none';
        trans_input.style.display = 'none';
    }
}


// Disabling the button after once click 
function disableButton_book(btn) {
    document.getElementById('submitRecord_book').disabled = true;
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