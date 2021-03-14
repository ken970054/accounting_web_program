function finalizeLogin(res) {
    res.user
    .getIdToken()
    .then(idToken => {
        console.log('[idToken]', idToken);
        // 把idToken寄送到後端(Flask)的某個API
        axios.post('/api/login', { idToken }, axiosConfig)
        .then(res => {
            console.log('[完成idToken資料傳遞]', res);
            // 重整畫面
            window.location.reload();
        })
        .catch(err => {
            console.log('[傳遞idToken失敗]', err);
        });
    })
}

$('#loginForm').submit(function (event) { //取得 id = '#loginForm' 的內容並執行submit function
    event.preventDefault(); // 避免畫面重新整理
    const form = {
        email: $('#loginEmail').val(),  //抓取 id = '#loginEmail' 的輸入文字
        password: $('#loginPassword').val(),
    };
    console.log('[登入]', form);
    firebase
        .auth()
        .signInWithEmailAndPassword(form.email, form.password)
        // 登入成功
        .then(res => {
            console.log('[成功登入]', res); // 將res print到chrome檢視console中方便觀察
            finalizeLogin(res);
        })
        // 登入失敗
        .catch(err => {
            console.log('[登入失敗]', err); 
            const code = err.code;
            if (code == "auth/wrong-password") {
                alert("密碼錯誤");
            } else if (code =="auth/user-not-found") {
                alert("無此Email");
            }

        });
});

$('#signUpForm').submit(function (event) {
    event.preventDefault();
    const form = {
        email: $('#signUpEmail').val(),
        password: $('#signUpPassword').val(),
    };
    console.log('[註冊]', form);
    firebase
        .auth()
        .createUserWithEmailAndPassword(form.email, form.password)
        .then(res => {
            console.log('[註冊成功]', res);
            finalizeLogin(res);
        })
        .catch(err => {
            console.log('[err]');
            alert(err.message);
        })

});

$('#logoutBtn').click(function () {
    console.log('[登出]');
    axios.post('/api/logout', {}, axiosConfig)
    .then(res => {
        // 引導回首頁
        window.location = '/'
    })
    .catch(err => {
        console.log('[err]', err);
        alert('出了錯誤，請重新嘗試');
    });
});