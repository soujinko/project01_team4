from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
SECRET_KEY = 'SPARTA'
client = MongoClient('52.78.209.2', 27017, username="test", password="test")
db = client.dbsparta_week1

# 메인페이지
@app.route('/')
def main():
    token_receive = request.cookies.get('mytoken')
    if token_receive is None:
        return render_template("main.html")
    else:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.users.find_one({'username': payload['id']})
            return render_template('main.html', user_info=user_info)
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login', msg='로그인 시간이 만료되었습니다.'))
        except jwt.exceptions.DecodeError:
            return redirect(url_for('login', msg='로그인 정보가 존재하지 않습니다.'))

# 회원가입 로그인
@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({'username': username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,
        "password": password_hash
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success' })

@app.route('/sign_in', methods=['POST'])
def sign_in():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': password_hash})
    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# 인덱스 페이지 카드들 정보 보내기기
@app.route('/getcard', methods=['GET'])
def get_card():
    type_receive = request.args.get('type_give')
    token_receive = request.cookies.get('mytoken')
    if token_receive:
        try:
            if type_receive == "coin":
                result = list(db.applist.find({'type': '코인거래소'}, {'_id': False}))
            else:
                result = list(db.applist.find({'type': '증권'}, {'_id': False}))
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.users.find_one({'username': payload['id']})
            return render_template('index.html', user_info=user_info, result=result )
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for("main"))
    else:
        if type_receive == "coin":
            result = list(db.applist.find({'type':'코인거래소'},{'_id':False}))
            return render_template("index.html", result=result)
        else:
            result = list(db.applist.find({'type': '증권'}, {'_id': False}))
            return render_template("index.html", result=result)


#리뷰정보 불러오기
@app.route('/detail_get_card', methods=['POST'])
def detail_get_card():
    title_receive = request.form['title_give']
    reviews = list(db.review.find({'app_name':title_receive},{'_id':False}))
    print(reviews)
    return jsonify({"result": "success", "reviews": reviews})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)