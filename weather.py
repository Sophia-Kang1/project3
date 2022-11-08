import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import config

url = "https://search.naver.com/search.naver?query=%EB%82%A0%EC%94%A8"
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')
#print(soup)

data1 = soup.find('div', {'class': 'weather_info'})

find_currenttemp = soup.find('div',{'class': 'temperature_text'}).text
print(find_currenttemp)

summary = soup.find('p', {'class': 'summary'}).text
print(summary)

data2 = data1.find_all('dd')
wind_chill = data2[0].text
humidity = data2[1].text
wind = data2[2].text
print('현재 체감온도: '+wind_chill)
print('현재 습도: '+humidity)
print('풍속: '+wind)

data3 = data1.find_all('li')
fine_dust = data3[0].text
ultrafine_dust = data3[1].text
uv_rays = data3[2].text
sunset = data3[3].text
print(fine_dust)
print(ultrafine_dust)
print(uv_rays)
print(sunset)

min_temp = soup.find('span', {'class': 'lowest'}).text
print(min_temp)
max_temp = soup.find('span', {'class': 'highest'}).text
print(max_temp)

weather = {
    'weather_info' : summary,
    'temp_now' : find_currenttemp,
    'min_temp' : min_temp,
    'max_temp' : max_temp,
    'wind_chill' : wind_chill,
    'humidity' : humidity,
    'wind_speed' : wind,
    'fine_dust' : fine_dust,
    'ultrafine_dust' : ultrafine_dust,
    'UV_rays' : uv_rays,
    'sunset' : sunset 
}

# pymongo
HOST = config.HOST
USER = config.USER
PASSWORD = config.PASSWORD
DATABASE_NAME = config.DATABASE_NAME
URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
client = MongoClient(URI)
db = client['project3']

# 크롤링 데이터 저장
db.naver_weather.insert_one(weather)