
from pymongo import MongoClient
client = MongoClient('52.78.209.2', 27017, username="test", password="test")
db = client.dbsparta_week1


# 리뷰별점 합계 앱리스트에 업데이트하기
# 리뷰 저장 시 추가 코드
star = db.applist.find_one({'app_name':'교보증권'})['star'] # 기존 별점
new_star = 4 # 새로 받아온 별점 합계
update_star = star + new_star
db.applist.update_one({'app_name':'코인빗'},{'$set':{'star':13}}) # 별점 업데이트



# 인덱스html 로그인시 불러올 코드
bestapps = list(db.applist.find({'type':'코인거래소'}).sort("star", -1).limit(3)) # 코인 별점 높은순으로 3개 불러오기
bestapps = list(db.applist.find({'type':'증권'}).sort("star", -1).limit(3)) # 증권 별점 높은순으로 3개 불러오기

