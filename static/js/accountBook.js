
$(document).ready(function() {

    // add, remove new record item
    $('#record_add').on('click', add);
    $('#record_remove').on('click', remove);

    function add(event) {
        event.preventDefault(); // 避免畫面重新整理
        var new_record_no = parseInt($('#total_record').val()) + 1;
        var new_record_item = document.getElementById('recordGroup_1').innerHTML;
        var new_record_item_after = '';
        
        // modify each id name by changing current number value
        var lines = new_record_item.split('\n');
        $.each(lines, function( index, line) {
            line = line.replace(/id="(\D+)\d"/, 'id="$1' + new_record_no + '"');
            line = line.replace(/"display: flex;"/, '"display: none;"'); // make sure the new added record will change "display:flex" to "display:none"
            line = line.replace(/$/, '\n');
            //console.log(line);
            new_record_item_after = new_record_item_after + line;
        });
        console.log(new_record_item_after);

        var add_item = "<div class='form-row justify-content-center' id='recordGroup_" + new_record_no +"' style='border-width:3px; border-style:solid; border-color:#D3D3D3; margin:15px; padding: 15px'>\n " + new_record_item_after +" \n</div>" 
        //console.log(add_item);
        if (new_record_no < 6) {
            //alert(new_record_item);
            $('#record_block').append(add_item);
            $('#total_record').val(new_record_no);

            //var record_block_check = document.getElementById('record_block').innerHTML;
            //console.log(record_block_check);
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
    var dict = [];
    for (let id_num = 1; id_num < 6; id_num++) {
        dict.push({
            Idx: id_num,
            ITI: 'incomeTypeInput_book_' + id_num.toString(10), 
            ETI: 'expendTypeInput_book_' + id_num.toString(10), 
            TTI: 'transTypeInput_book_' + id_num.toString(10), 
            IM: 'inputMoney_book_' + id_num.toString(10), 
            CM: 'costMoney_book_' + id_num.toString(10), 
            TA: 'transAmount_book_' + id_num.toString(10),
            IM_M: 'inputMoney_message_book_' + id_num.toString(10), 
            CM_M: 'costMoney_message_book_' + id_num.toString(10), 
            TA_M: 'transAmount_message_book_' + id_num.toString(10)
        });
        //$('#recordGroup_' + i).find('#inputTransType_book_' + i).on('change', dict, show_transType_account);
    }
    $('#record_block').on('change', '#inputTransType_book_1', dict[0], show_transType_account);
    $('#record_block').on('change', '#inputTransType_book_2', dict[1], show_transType_account);
    $('#record_block').on('change', '#inputTransType_book_3', dict[2], show_transType_account);
    $('#record_block').on('change', '#inputTransType_book_4', dict[3], show_transType_account);
    $('#record_block').on('change', '#inputTransType_book_5', dict[4], show_transType_account);
    

    function show_transType_account(event) {
        var transType = this.value;
        //var selectID = this.id;
        console.log(event.data.ITI);
        var income_input = document.getElementById(event.data.ITI);
        var expend_input = document.getElementById(event.data.ETI);
        var trans_input = document.getElementById(event.data.TTI);
        
    
        if (transType === "Income"){
            income_input.style.display = 'flex';
            expend_input.style.display = 'none';
            trans_input.style.display = 'none';
            
            document.querySelector('#' + event.data.IM).onkeyup = function() {
                var inputMoney = document.querySelector('#' + event.data.IM).value;
                if (inputMoney === "") {
                    document.querySelector('#submitRecord_book').disabled = true;
                    document.getElementById(event.data.IM_M).innerHTML = "Please enter money.";
                }
                else {
                    document.querySelector('#submitRecord_book').disabled = false;
                    document.getElementById(event.data.IM_M).innerHTML = "";
                }
            }
        }
        else if (transType === "Expense"){
            income_input.style.display = 'none';
            expend_input.style.display = 'flex';
            trans_input.style.display = 'none';

            document.querySelector('#' + event.data.CM).onkeyup = function() {
                var inputMoney = document.querySelector('#' + event.data.CM).value;
                if (inputMoney === "") {
                    document.querySelector('#submitRecord_book').disabled = true;
                    document.getElementById(event.data.CM_M).innerHTML = "Please enter money.";
                }
                else {
                    document.querySelector('#submitRecord_book').disabled = false; 
                    document.getElementById(event.data.CM_M).innerHTML = "";
                }
            }
        }
        else if (transType === "Transfer"){
            income_input.style.display = 'none';
            expend_input.style.display = 'none';
            trans_input.style.display = 'flex';

            document.querySelector('#' + event.data.TA).onkeyup = function() {
                var inputMoney = document.querySelector('#' + event.data.TA).value;
                if (inputMoney === "") {
                    document.querySelector('#submitRecord_book').disabled = true;
                    document.getElementById(event.data.TA_M).innerHTML = "Please enter money.";
                }
                else {
                    document.querySelector('#submitRecord_book').disabled = false; 
                    document.getElementById(event.data.TA_M).innerHTML = "";
                }
            }
        }
        else {
            income_input.style.display = 'none'; 
            expend_input.style.display = 'none';
            trans_input.style.display = 'none';
        }
    }

    //Timestamp hide/show checkbox setting
    $('#checkbox_id').on('click', '#timeStampSwitch', checkbox_switch);
    function checkbox_switch() {
            console.log("checked??");
            if($("#timeStampSwitch").prop("checked")) {
                $("#accountBook_table").find("td:nth-child(8),th:nth-child(8)").show();
            } else {
                $("#accountBook_table").find("td:nth-child(8),th:nth-child(8)").hide();
            }
    }
    




});





// Disabling the button after clicking once 
function disableButton_book(btn) {
    document.getElementById('submitRecord_book').disabled = true;
}

// fetch form data and post to Flask
$('#record_form').submit(function (event) {
    event.preventDefault(); // 避免畫面重新整理
    
    const form = {};
    for (let id_num = 1; id_num <= 5; id_num++) {
        //type
        var type_id = 'inputTransType_book_' + id_num.toString(10);
        //ITI_id = 'incomeTypeInput_book_' + id_num.toString(10); 
        //ETI_id = 'expendTypeInput_book_' + id_num.toString(10); 
        //TTI_id = 'transTypeInput_book_' + id_num.toString(10); 
        
        //month
        var month_id = 'inputMonth_book_' + id_num.toString(10);
        
        //item
        var II_id = 'incomeItem_book_' + id_num.toString(10);
        var EI_id = 'expendItem_book_' + id_num.toString(10);

        //money
        var IM_id = 'inputMoney_book_' + id_num.toString(10); 
        var CM_id = 'costMoney_book_' + id_num.toString(10); 
        var TA_id = 'transAmount_book_' + id_num.toString(10);

        //account
        var IA_id = 'incomeAccount_book_' + id_num.toString(10);
        var EA_id = 'expendAccount_book_' + id_num.toString(10);
        var WA_id = 'withdrawAccount_book_' + id_num.toString(10);
        var DA_id = 'depositAccount_book_' + id_num.toString(10);

        //note
        var IN_id = 'incomeNote_book_' + id_num.toString(10);
        var EN_id = 'expendNote_book_' + id_num.toString(10);
        var TN_id = 'transNote_book_' + id_num.toString(10);

        //把所有內容加到dict當中
        var transType = $('#' + type_id).val();
        if (transType === "Income"){
            form['transactionType_book_' + id_num.toString(10)] = transType;
            form['month_book_' + id_num.toString(10)] = $('#' + month_id).val();
            form['incomeItem_book_' + id_num.toString(10)] = $('#' + II_id).val();
            form['amountOfMoney_book_' + id_num.toString(10)] = $('#' + IM_id).val();
            form['incomeAccount_book_' + id_num.toString(10)] = $('#' + IA_id).val();
            form['incomeNote_book_' + id_num.toString(10)] = $('#' + IN_id).val();
        }
        else if (transType === "Expense") {
            form['transactionType_book_' + id_num.toString(10)] = transType; 
            form['month_book_' + id_num.toString(10)] = $('#' + month_id).val();
            form['expendItem_book_' + id_num.toString(10)] = $('#' + EI_id).val();
            form['amountOfMoney_book_' + id_num.toString(10)] = $('#' + CM_id).val();
            form['expendAccount_book_' + id_num.toString(10)] = $('#' + EA_id).val();
            form['expendNote_book_' + id_num.toString(10)] = $('#' + EN_id).val();
        }
        else if (transType === "Transfer") {
            form['transactionType_book_' + id_num.toString(10)] = transType; 
            form['month_book_' + id_num.toString(10)] = $('#' + month_id).val();
            form['withdrawAccount_book_' + id_num.toString(10)] = $('#' + WA_id).val();
            form['transAmount_book_' + id_num.toString(10)] = $('#' + TA_id).val();
            form['depositAccount_book_' + id_num.toString(10)] = $('#' + DA_id).val();
            form['transNote_book_' + id_num.toString(10)] = $('#' + TN_id).val();
        }
    }
    console.log(form);

    const path = '/account/book';
    //post to Flask
    axios.post(path, form, axiosConfig)
        .then(res => {
           console.log('[完成form傳遞]', form);
           window.location.reload();
        })
        .catch(err => {
            console.log('[傳遞form失敗]', err);
        });
});