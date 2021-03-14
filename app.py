
import firebase_admin
import os
from firebase_admin import credentials, firestore, auth
from flask_wtf import CSRFProtect

cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
# 建立資料庫的實例(db)
db = firestore.client()

import time
import datetime

# 引用flask相關資源
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, abort
# 引用各種表單類別
from forms import CreateProductForm, EditProductForm, DeleteProductForm, CreateCommentForm, UpdateCommentForm

app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)

# 設定應用程式的SECRET_KEY
app.config['SECRET_KEY'] = 'abc12345678'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
cookie_name = 'flask_cookie'

@app.context_processor
def check_login():
    print("[check_login]")
    # 取得session_cookie
    session_cookie = request.cookies.get(cookie_name)
    ###print("[session_cookie]", session_cookie)
    # 預設登入狀態
    auth_state = {
        # 是否登入
        "is_login": False,
        # 是否為管理者
        "is_admin": False,
        # 資料
        "user": {}
    }
    # 準備驗證
    try:
        # 驗證session_cookie
        user_info = auth.verify_session_cookie(session_cookie, check_revoked=True)
        # 將資料存到登入狀態內
        auth_state["user"] = user_info
        # 取得user email
        email = user_info['email']
        # 取得 admin_list/{email} 文件
        admin_doc = db.document(f'admin_list/{email}').get()
        # 判斷admin_doc是否存在
        if admin_doc.exists:
            auth_state["is_admin"] = True
        # 標記此人為登入狀態
        auth_state["is_login"] = True
    except:
        # 未登入
        print('[用戶未登入]')
    # 把auth_state傳遞到各個模板內
    return dict(auth_state=auth_state)

@app.before_request
def guard():
    auth_state = check_login()['auth_state']
    # 指向使用者所導入的路由函數名稱
    endpoint = request.endpoint
    is_admin = auth_state['is_admin']
    # 受管理者權限保護的頁面
    admin_route_list = [
        'create_product_page',
        'edit_product_page'
    ]
    # 如果造訪的頁面是
    # 管理者權限保護頁面，而且此人並非管理者
    if endpoint in admin_route_list and not is_admin:
        # 強制回首頁
        return redirect('/')

@app.route('/')
def index_page():
    # 取得資料庫的商品列表(product_list)資料
    collection = db.collection('product_list').order_by(
        'created_at', direction='DESCENDING').get()
    # 定義產品列表
    product_list = []
    # 把這個集合內的文件取出
    for doc in collection:
        # print('[doc]', doc)
        # 取得文件內的資料(字典)
        # print('[doc.to_dict()]', doc.to_dict())
        product = doc.to_dict()
        # print('[文件的ID]', doc.id)
        # 取得文件的ID並存到product內
        product['id'] = doc.id
        # print('[商品]', product)
        product_list.append(product)
    # 首頁路由
    return render_template('index.html', product_list=product_list)

@app.route('/api/login', methods=['POST'])
def login():
    print('準備開始登入API流程')
    # 取得前端傳給後端的資料
    id_Token = request.json['idToken']
    print('[id_token]', id_Token)
    # 過期日
    expires_in = datetime.timedelta(days=7)
    try:
        # 產生session_cookie
        session_cookie = auth.create_session_cookie(id_Token, expires_in=expires_in)
        print('[session_cookie]', session_cookie)
        # 準備要回應給前端JS的資訊
        res = jsonify({
            'msg': 'OK'
        })
        expires = datetime.datetime.now() + expires_in
        # 將session_cookie寫入至使用者的瀏覽器內
        res.set_cookie(cookie_name, session_cookie, expires=expires, httponly=True)
        return res
    except:
        return abort(401, "IDToken失效或Firebase Server目前出狀況")

@app.route('/api/logout', methods=['POST'])
def logout():
    # 讓指定的cookie失效
    res = jsonify({ 'msg': 'OK'})
    res.set_cookie(cookie_name, expires=0)
    return res

@app.route('/product/create', methods=['GET', 'POST'])
def create_product_page():
    # 建立商品頁的路由

    # 建立商品表單的實例
    form = CreateProductForm()
    # 設定表單送出後的處理
    if form.validate_on_submit():
        print('[新增商品表單被送出且沒有問題]')
        new_product = {
            'title': form.title.data,
            'img_url': form.img_url.data,
            'category': form.category.data,
            'price': form.price.data,
            'on_sale': form.on_sale.data,
            'description': form.description.data,
            'created_at': time.time()
        }
        print('[新增的商品]', new_product)
        # 把new_product存到資料庫內一個名為product_list的集合內
        db.collection('product_list').add(new_product)
        # 取得轉跳頁面的網址
        redirect_url = url_for('create_finished_page')
        print('[轉跳新頁面]', redirect_url)
        # 將新商品的資料儲存在session內以便下個頁面可顯示新資料
        # 把new_product存到session
        session['new_product'] = new_product
        # 回傳轉跳程序
        return redirect(redirect_url)
    return render_template('product/create.html', form=form)


@app.route('/product/create-finished')
def create_finished_page():
    # 從session取得new_product
    new_product = session['new_product']
    # 商品建立成功的路由
    return render_template('product/create_finished.html', new_product=new_product)


@app.route('/product/<pid>/show', methods=['GET', 'POST'])
def show_product_page(pid):
    # 商品詳情頁的路由
    
    # 取得資料庫指定pid的商品資料
    doc = db.collection('product_list').document(pid).get()
    product = doc.to_dict()
    product['id'] = doc.id
    # 新增留言表單
    create_comment_form = CreateCommentForm()
    # 如果表單被送出且合法
    if create_comment_form.validate_on_submit():
        new_comment = {
            'email': create_comment_form.email.data,
            'content': create_comment_form.content.data,
            'created_at': time.time()
        }
        # 把新留言存放到 product_list(集合)/pid(文件)/comment_list(集合)
        db.collection(f'product_list/{pid}/comment_list').add(new_comment)
        return redirect(f'/product/{pid}/show')
    # 取得所有該商品的留言
    comment_collection = db.collection(
        f'product_list/{pid}/comment_list').order_by('created_at', direction='DESCENDING').get()
    # 留言列表
    comment_list = []
    # 取得留言集合內的所有文件
    for doc in comment_collection:
        comment = doc.to_dict()
        comment['id'] = doc.id
        # 把更新留言的表單存到留言內
        comment['form'] = UpdateCommentForm(prefix=doc.id)
        # 如果更新留言被送出且合法
        if comment['form'].validate_on_submit():
            updated_comment = {
                'content': comment['form'].content.data
            }
            # 把新留言更新到資料庫內
            db.document(f'product_list/{pid}/comment_list/{doc.id}').update(updated_comment)
            return redirect(f'/product/{pid}/show')
        # 把表單內容輸入值預設為留言的內容
        comment['form'].content.data = comment['content']
        # 將一篇留言推送到留言列表內
        comment_list.append(comment)
    return render_template('product/show.html', 
                            product=product, 
                            create_comment_form=create_comment_form, 
                            comment_list=comment_list)
    

@app.route('/product/<pid>/edit', methods=['GET', 'POST'])
def edit_product_page(pid):
    # 編輯商品頁的路由
    # 取得資料庫指定pid的商品資料
    doc = db.collection('product_list').document(pid).get()
    product = doc.to_dict()
    product['id'] = pid
    print('[商品資料]', product)
    # 建立刪除商品表單的實例
    delete_form = DeleteProductForm()
    if delete_form.validate_on_submit():
        # 從product_list集合內移除一個ID為pid的文件
        db.collection('product_list').document(pid).delete()
        # 轉跳回首頁
        return redirect('/')
    # 建立編輯商品表單的實例
    form = EditProductForm()
    if form.validate_on_submit():
        print('[準備進入商品更新流程]')
        updated_product = {
            'title': form.title.data,
            'img_url': form.img_url.data,
            'price': form.price.data,
            'category': form.category.data,
            'on_sale': form.on_sale.data,
            'description': form.description.data
        }
        db.collection('product_list').document(pid).update(updated_product)
        # 轉跳到首頁
        redirect_url = url_for('index_page')
        return redirect(redirect_url)
    # 把目前商品的值寫入到表單裡作為預設值
    form.title.data = product['title']
    form.img_url.data = product['img_url']
    form.price.data = product['price']
    form.category.data = product['category']
    form.on_sale.data = product['on_sale']
    form.description.data = product['description']
    return render_template('product/edit.html', form=form, delete_form=delete_form, product=product)


if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    dev_host = '127.0.0.1'
    heroku_host = '0.0.0.0'

    # 應用程式開始運行
    app.run(debug=True, host=heroku_host, port=port)
