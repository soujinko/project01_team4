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
                bestapps = list(db.applist.find({'type': '코인거래소'}).sort("star", -1).limit(3))
                for i in bestapps:
                    i['review'] = db.review.count_documents({'app_name': i['app_name']})
                    if (i['review']):
                        review = i['review']
                        star = i['star']
                        i['star_avg'] = round(star / review, 1)
                for i in result:
                    i['review'] = db.review.count_documents({'app_name': i['app_name']})
                    if (i['review']):
                        review = i['review']
                        star = i['star']
                        i['star_avg'] = round(star / review, 1)
            else:
                result = list(db.applist.find({'type': '증권'}, {'_id': False}))
                bestapps = list(db.applist.find({'type': '증권'}).sort("star", -1).limit(3))
                for i in bestapps:
                    i['review'] = db.review.count_documents({'app_name': i['app_name']})
                    if (i['review']):
                        review = i['review']
                        star = i['star']
                        i['star_avg'] = round(star / review, 1)
                for i in result:
                    i['review'] = db.review.count_documents({'app_name': i['app_name']})
                    if (i['review']):
                        review = i['review']
                        star = i['star']
                        i['star_avg'] = round(star / review,1)
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.users.find_one({'username': payload['id']})

            return render_template('index.html', user_info=user_info, result=result, type=type_receive, bestapps= bestapps)
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for("main"))
    else:
        if type_receive == "coin":
            result = list(db.applist.find({'type':'코인거래소'},{'_id':False}))
            for i in result:
                i['review'] = int(db.review.count_documents({'app_name': i['app_name']}))
                if (i['review'] ):
                    review = i['review']
                    star = i['star']
                    i['star_avg'] = round(star / review, 1)
            return render_template("index.html", result=result , type=type_receive)
        else:
            result = list(db.applist.find({'type': '증권'}, {'_id': False}))
            for i in result:
                i['review'] = db.review.count_documents({'app_name': i['app_name']})
                if (i['review']):
                    review = i['review']
                    star = i['star']
                    i['star_avg'] = round(star / review, 1)
            return render_template("index.html", result=result , type=type_receive)


# index.html에서 선택한 카드 세부 정보 detail.html에 보내기
@app.route('/get_detail_Test', methods=['GET'])
def get_detail_card():
    token_receive = request.cookies.get('mytoken')
    if token_receive:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.users.find_one({'username': payload['id']})
            type_receive = request.args.get('type_give')
            result = db.applist.find_one({'app_name': type_receive})
            result2 = list(db.review.find({'app_name': type_receive}, {'_id': False}))
            if result2:
                count = db.review.count_documents({'app_name': type_receive})
                print(count)
                star_1 = 0
                star_2 = 0
                star_3 = 0
                for i in result2:
                    star_1 += i['star1']
                    star_2 += i['star2']
                    star_3 += i['star3']
                star_4 = star_1 + star_2 + star_3
                star1 = round(star_1/count, 1)
                star2 = round(star_2/count, 1)
                star3 = round(star_3/count, 1)
                star4 = round(star_4/3/count, 1)
                return render_template("detail.html", result=result, result2=result2, user_info=user_info, star1=star1, star2=star2, star3=star3, star4=star4 )
            else:
                return render_template("detail.html", result=result, result2=result2, user_info=user_info)
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for("main"))
    else:
        type_receive = request.args.get('type_give')
        result = db.applist.find_one({'app_name': type_receive})
        result2 = list(db.review.find({'app_name': type_receive}, {'_id': False}))
        if result2:
            count = db.review.count_documents({'app_name': type_receive})
            print(count)
            star_1 = 0
            star_2 = 0
            star_3 = 0
            for i in result2:
                star_1 += i['star1']
                star_2 += i['star2']
                star_3 += i['star3']
            star_4 = star_1 + star_2 + star_3
            star1 = round(star_1 / count, 1)
            star2 = round(star_2 / count, 1)
            star3 = round(star_3 / count, 1)
            star4 = round(star_4 / 3 / count, 1)
            return render_template("detail.html", result=result, result2=result2, star1=star1,
                                   star2=star2, star3=star3, star4=star4)
        else:
            return render_template("detail.html", result=result, result2=result2)


#detail.html에서 작성한 리뷰 review DB에 저장
@app.route('/review', methods=['POST'])
def write_review():
    appname_receive = request.form['appname_give']
    username_receive = request.form['username_give']
    comment_receive = request.form['comment_give']
    star1 = int(request.form['star1_give'])
    star2 = int(request.form['star2_give'])
    star3 = int(request.form['star3_give'])

    star4 = (star1 + star2 + star3)/3
    star = db.applist.find_one({'app_name': appname_receive})['star']
    new_star = star4 + star
    db.applist.update_one({'app_name': appname_receive}, {'$set': {'star': new_star}})

    doc={
        'username': username_receive,
        'app_name': appname_receive,
        'comment': comment_receive,
        'star1': star1,
        'star2': star2,
        'star3': star3
    }
    db.review.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})

# 사용자 리뷰 불러오기
@app.route('/user/<username>')
def user(username):

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        reviews = list(db.review.find({'username': username},{'_id':False}))
        user_info = db.users.find_one({"username": payload['id']}, {"_id": False})
        count = db.review.count_documents({'username': username})
        return render_template('user.html', user_info=user_info, reviews=reviews, count=count)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("main"))

@app.route('/delete', methods=['POST'])
def delete():
    username_receive = request.form['username_give']
    appname_receive = request.form['appname_give']
    db.review.delete_one({'username': username_receive, 'app_name':appname_receive})
    return jsonify({'msg': f'{appname_receive} 리뷰를 삭제했습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)