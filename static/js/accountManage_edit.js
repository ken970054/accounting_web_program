


// Disabling the button after once click 
function disableAccountDepositButton(btn) {
    document.getElementById('accountManage_depositModify').disabled = true;
}


// Pass edit data to backend
$('#AccountDepositDataForm').submit(function (event) {
    event.preventDefault(); // 避免畫面重新整理

    var depositMoney = $("#depositMoney").val();
    var selected_year = $("#checkYear").text();
    var account_name = $("#account_deposit_group").parent().find(".card-header").html();
    account_name = account_name.match(/>(.+)<\/span>/);  // () match is in account_name[1]

    const form =  {
        Original_deposit: depositMoney,
        selected_year: selected_year,
        account_name: account_name[1]
    };
    const path = '/account_manage';
    axios.post(path, form, axiosConfig)
        .then(res => {
            console.log('[完成form傳遞]', form);
            window.location.reload();
        })
        .catch(err => {
            console.log('[傳遞form失敗]', err);
        });

});