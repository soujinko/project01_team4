import openpyxl
from pymongo import MongoClient
client = MongoClient('52.78.209.2', 27017, username="test", password="test")
db = client.dbsparta_week1

wb = openpyxl.load_workbook("C:\\Users\\souji\\Desktop\\bootcamp\\file\\applist.xlsx")
wb_sheet = wb.active

for row in wb_sheet:
    type = row[2].value
    if type is not None:
        company = row[3].value
        app_name = row[4].value
        image_url = row[5].value
        google_url = row[6].value
        doc = {
            'type': type,
            'company': company,
            'app_name': app_name,
            'image_url': image_url,
            'google_url': google_url,
            'star': 0
        }
        print(doc)
        db.applist.insert_one(doc)

wb.close()