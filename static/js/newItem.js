// add new item form when clicking the buttom

// fetch form data and post to Flask
$('#incomeCostAdding').submit(function (event) {
    event.preventDefault(); // 避免畫面重新整理
    
    var transType = $('#inputTransType').val();
    if (transType === "Income"){
        const form =  {
            transactionType: transType,
            month: $('#inputMonth').val(),
            incomeItem: $('#incomeItem').val(),
            amountOfMoney: $('#inputMoney').val(),
            incomeAccount: $('#incomeAccount').val(),
            incomeNote: $('#incomeNote').val(),
        };
        console.log(form);
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
            transactionType: transType,
            month: $('#inputMonth').val(),
            expendItem: $('#expendItem').val(),
            amountOfMoney: $('#costMoney').val(),
            expendAccount: $('#expendAccount').val(),
            expendNote: $('#expendNote').val(),
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
            transactionType: transType,
            month: $('#inputMonth').val(),
            withdrawAccount: $('#withdrawAccount').val(),
            transAmount: $('#transAmount').val(),
            depositAccount: $('#depositAccount').val(),
            transNote: $('#transNote').val(),
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


