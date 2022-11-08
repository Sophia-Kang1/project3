from bs4 import BeautifulSoup
from urllib.request import urlopen
import config
from pymongo import MongoClient

# url 설정
html = urlopen("https://www.musinsa.com/category/001001")
bs = BeautifulSoup(html, 'html.parser')
print(bs)

item_list = bs.find_all('li', {'class':'li_box'})
print(item_list)

brand = []
name = []
price = []

for item in item_list:
    
    brand_box = item.find_all('p', {'class':'item_title'})
    if len(brand_box) == 1:
        brand.append(brand_box[0].get_text())
    elif len(brand_box) == 2 :
        brand.append(brand_box[1].get_text())
        
    name_box = item.find('a', {'class':'img-block'}).get('title')
    name.append(name_box.strip())
    
    price_box = item.find('p', {'class':'price'}).get_text().split()
    if len(price_box) == 1:
        price.append(price_box[0])
    elif len(price_box) == 2:
        price.append(price_box[1])

import pandas as pd

data = {'브랜드':brand, '상품명':name, '가격'+'('+'할인가'+')':price}

df=pd.DataFrame(data)

df.to_csv('./item.csv')

# pymongo
HOST = config.HOST
USER = config.USER
PASSWORD = config.PASSWORD
DATABASE_NAME = config.DATABASE_NAME
URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
client = MongoClient(URI)
db = client['project3']
item_db = db["item"]
# 크롤링 데이터 저장
db.item_db.insert_one(data)