import openpyxl
from pymongo import MongoClient
client = MongoClient('aws ip', 27017, username="test", password="test") #자신의 aws ip 입력
db = client.dbsparta_week1

wb = openpyxl.load_workbook("C:\\Users\\souji\\Desktop\\bootcamp\\file\\applist2.xlsx") #엑셀파일 경로
wb_sheet = wb.active

for row in wb_sheet:
    type = row[2].value
    if type is not None:
        company = row[3].value
        app_name = row[4].value
        image_url = row[5].value
        google_url = row[6].value
        doc = {
            'type': type, #코인, 증권 타입
            'company': company, #회사명
            'app_name': app_name, #어플리케이션명
            'image_url': image_url, #이미지 경로
            'google_url': google_url #구글 플레이스토어 경로
        }
        print(doc)
        db.applist.insert_one(doc)

wb.close()