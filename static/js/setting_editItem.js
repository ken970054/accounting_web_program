
$(document).ready(function() {
    
    // read edit item's date and time and input to editItem_modal
    $("#accountSetting, #incomeItemSetting, #expenseItemSetting").on('click','.btn-primary',function() {
        var ModalId = ($(this).data("target")); // get Modal id when clicked 
        
        // get title data and change to modal header title
        var currentDiv = $(this).parent().parent();
        var currentTitle = currentDiv.find('.card-header').text();
        
        var lines = currentTitle.split('\n'); // deal with the space and space line
        lines.forEach(function(line) {
            let trimstr = line.trim();
            if (trimstr !== ""){
                currentTitle = trimstr;
            }
        });
        $(ModalId).find("h5.modal-title").text("Modifing " + currentTitle);
   
    });

    // switch the clicked button in account group and delete group
    $('#account_button_group, #income_button_group, #expense_button_group').on('click', 'button', move_button_toDelete);
    function move_button_toDelete (event) {
        var value = $(event.target).attr("value");

        // get delete button group id
        var parent_id = $(event.target).parent().attr("id");
        var delete_div_id = "delete_" + parent_id;
        
        // get modify button id
        var modify_button_id = $(event.target).parent().parent().parent().parent().find(".modal-footer").children().attr("id");
        modify_button_id = "#" + modify_button_id;

        var warning_message = "If you delete " + value + ", all your related record will be erased!!"
        var isMove = confirm(warning_message);
        if (isMove) {
            $(event.target).remove();
            document.getElementById(delete_div_id).innerHTML += '<button type="button" class="btn btn-outline-secondary" style="margin-top: 5px; margin-left: 5px" value="' + value + '">' + value + '</button>';

            var delete_button_element = "#" + delete_div_id + " > button";
            if ($(delete_button_element).length) {
                $(modify_button_id).prop("disabled",false);
            }
        }
    }

    $('#delete_account_button_group, #delete_income_button_group, #delete_expense_button_group').on('click', 'button', undo_button_to);
    function undo_button_to (event) {
        var value = $(event.target).attr("value");
        var warning_message = "Undo " + value + " to your account";

        // get current_button_group id, delete_button_group id, add_button_group id
        var parent_id = $(event.target).parent().attr("id");  // delete_button_group
        var current_id = parent_id.replace(/^[^_]+_(?=[^_])/, '');  // match everything before first underscore and include the underscore 
        var add_id = "add_" + current_id; //add_button_group

        // get modify button id
        var modify_button_id = $(event.target).parent().parent().parent().parent().find(".modal-footer").children().attr("id");
        modify_button_id = "#" + modify_button_id;
    
        var isMove = confirm(warning_message);
        if (isMove) {
            $(event.target).remove();
            document.getElementById(current_id).innerHTML += '<button type="button" class="btn btn-outline-secondary" style="margin-top: 5px; margin-left: 5px" value="' + value + '">' + value + '</button>';

            var delete_button_element = "#" + parent_id + " > button";
            var add_button_element = "#" + add_id + " > button";
            // disable if both add_button_group and delete_button_group have no button element
            if (!$(add_button_element).length && !$(delete_button_element).length) {
                $(modify_button_id).prop("disabled",true);
            }
            
        }
    }

    // enter input and add to add_button_group
    $('#enterAccount, #enterIncomeItem, #enterExpenseItem').on('click', 'button', add_button_to);
    function add_button_to (event) {
        var userInput = $(event.target).parent().find("input");
        var userInput_text = userInput.val();

        // get current group id and its button group element
        var current_id = $(event.target).parent().parent().attr("id");
        current_id = current_id.replace(/enter/,'');
        final_current_id = "#current" + current_id;
        var current_button_group_id = $(final_current_id).find(".card-body").attr("id");
        var current_button_group_container = document.querySelector('#' + current_button_group_id);
        var current_button_group = current_button_group_container.querySelectorAll(".btn");
        
        // get delete button group id and its button group element
        delete_id = "#delete" + current_id;
        var delete_button_group_id = $(delete_id).find(".card-body").attr("id");
        var delete_button_group_container = document.querySelector('#' + delete_button_group_id);
        var delete_button_group = delete_button_group_container.querySelectorAll(".btn");
        
        // get add button group id
        var add_id = current_id = "#add" + current_id;
        var add_button_group_id = $(add_id).find(".card-body").attr("id");

        // get modify button id
        var modify_button_id = $(event.target).parent().parent().parent().parent().parent().find(".modal-footer").children().attr("id");
        modify_button_id = "#" + modify_button_id;


        // get modal title and eliminate the first word
        var currentTitle = $(event.target).parent().parent().parent().parent().find(".modal-title").text();
        currentTitle = currentTitle.replace(/^[^\s]+\s(?=[^\s])/,'') // replace the first word with empty string 

        var letters = /^[A-Za-z0-9 ]+$/;
        if (userInput_text.match(letters) && userInput_text.length <= 20 && userInput_text.length >= 3) {
            // get value from each current button and compare with the user input
            for (i = 0; i < current_button_group.length; i++) {
            //console.log(current_button_group[i].value);
                if (userInput_text.toLowerCase() === current_button_group[i].value.toLowerCase()) {
                    alert("You already have the same " + currentTitle + "!");
                    return;
                }
            }
            // get value from each delete button and compare with the user input
            for (i = 0; i < delete_button_group.length; i++) {
                console.log(delete_button_group[i].value);
                if (userInput_text.toLowerCase() === delete_button_group[i].value.toLowerCase()) {
                    alert("You already have the same " + currentTitle + "!");
                    return;
                }
            }

            var warning_message = "Add " + userInput_text + " to your " + currentTitle;
            var isMove = confirm(warning_message);
            if (isMove) {
                document.getElementById(add_button_group_id).innerHTML += '<button type="button" class="btn btn-outline-secondary" style="margin-top: 5px; margin-left: 5px" value="' + userInput_text + '">' + userInput_text + '</button>';
                userInput.val(''); //clean input text area
                
                if ($("#" + add_button_group_id + " > button").length) {
                    $(modify_button_id).prop("disabled",false);
                }
            }
        }
        else {
            alert("Please enter only character and digit, and not exceed to 20 characters!");
        }
        
    }

    //cancel add account button
    $('#add_account_button_group, #add_income_button_group, #add_expense_button_group').on('click', 'button', cancel_add_button);
    function cancel_add_button (event) {
        // get add button group id
        var add_id = $(event.target).parent().attr("id");
        
        // get delete button
        var delete_id = add_id.replace(/^[^_]+(?=_)/,'delete');

        // get modify button id
        var modify_button_id = $(event.target).parent().parent().parent().parent().find(".modal-footer").children().attr("id");
        modify_button_id = "#" + modify_button_id;

        $(event.target).remove();

        // disable if both add_button_group and delete_button_group have no button element
        if (!$("#" + add_id + " > button").length && !$("#" + delete_id + " > button").length) {
            $(modify_button_id).prop("disabled",true);
        }
    }

});

// Disabling the button after once click 
function disableModifyButton(btn) {
    document.getElementById('account_modifySetting').disabled = true;
    document.getElementById('income_modifySetting').disabled = true;
    document.getElementById('expense_modifySetting').disabled = true;
}


// Pass edit data to backend
$('#settingAccountDataForm, #settingIncomeDataForm, #settingExpenseDataForm').submit(function (event) {
    event.preventDefault(); // 避免畫面重新整理
    
    var formType = $(this).attr("id");
    // get delete dict
    var delete_button_group_id = $(this).children(".modal-body").children("[id^=delete]").children(".card-body").attr("id");
    var delete_button_group_container = document.querySelector('#' + delete_button_group_id);
    var delete_button_group = delete_button_group_container.querySelectorAll(".btn");
    const dict_delete = {};
    for (i = 0; i < delete_button_group.length; i++) {
        dict_delete[delete_button_group[i].value] = delete_button_group[i].value;
    }

    // get add dict
    var add_button_group_id = $(this).children(".modal-body").children("[id^=add]").children(".card-body").attr("id");
    var add_button_group_container = document.querySelector('#' + add_button_group_id);
    var add_button_group = add_button_group_container.querySelectorAll(".btn");
    const dict_add = {};
    for (i = 0; i < add_button_group.length; i++) {
        dict_add[add_button_group[i].value] = add_button_group[i].value;
    }

    const form =  {
        form_type: formType,
        delete_list: dict_delete,
        add_list: dict_add
    };

    const path = '/account_setting';
    axios.post(path, form, axiosConfig)
        .then(res => {
            console.log('[完成form傳遞]', form);
            window.location.reload();
        })
        .catch(err => {
            console.log('[傳遞form失敗]', err);
        });
    

});