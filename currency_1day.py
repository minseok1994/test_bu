import requests 
import pandas as pd
from tqdm import tqdm 
import os
if os.path.isdir("./currency") == False:
    os.mkdir("./currency")
url= "https://spib.wooribank.com/pib/jcc?withyou=CMCOM0184&__ID=c012238"
import pandas as pd
from datetime import timedelta

# 오늘 날짜 가져오기
from datetime import datetime, timedelta
# 현재 날짜 및 시간 객체 생성
# 현재 날짜 및 시간 객체 생성
today = datetime.now()

# 어제 날짜 계산
yesterday = today - timedelta(days=1)

# 시작 날짜
start_date = pd.to_datetime(today)

# 목표 날짜 (현재 날짜로 가정)
end_date = pd.to_datetime(today)

# 년, 월, 일을 저장할 리스트
years = []
months = []
days = []

# 날짜를 1씩 증가시키면서 평일인지 확인
current_date = start_date
while current_date <= end_date:
    # 현재 날짜가 평일이면 리스트에 추가
    if current_date.weekday() < 5:
        years.append(current_date.year)
        months.append(current_date.month)
        days.append(current_date.day)
    
    # 날짜를 1일씩 증가
    current_date += timedelta(days=1)

# 결과 출력
# for year, month, day in zip(years, months, days):
#     print(f"{year}.{month:02d}.{day:02d}")

from tqdm import tqdm
from io import StringIO

new_columns = ['currency_symbol','currency_name', 'sell', 'buy', 'buy_cash', 'buy_cash_rate','sell_cash', 'sell_cash_rate',  'exchange_Rate_selling', 'base_rate', 'Conversion Rate to USD', 'date' ]

currency_trade_list=[]
url= "https://spib.wooribank.com/pib/jcc?withyou=CMCOM0184&__ID=c012238"
for i in tqdm(range(len(years))):
  payload = {"BAS_DT_601":"20240115",
  "NTC_DIS":"A",
  "INQ_DIS_601":"",
  "NTC_DIS":"A",
  "SELECT_DATE_601":f"{years[i]}.{months[i]}.{days[i]}",
  "SELECT_DATE_601Y":f"{years[i]}",
  "SELECT_DATE_601M":f"{months[i]}",
  "SELECT_DATE_601D":f"{days[i]}",}


# print("hello seongcheol shichi's world");
# print("i am hogu mungchungyi");
# print("i am JJAP choi woo sik");
# print("ang gimochi");
# print("bal bbajin jwi, bal bbajin jwi");
# print("이번역은 슈크림 도어 사이가 넓으니 쥐하시길 바랍니다")
# print("슈크림 먹고싶다 슈붕");
# print("근데 사실 나는 슈붕보다 팥붕임ㅅㄱ");


  try:
    r = requests.post(url, data=payload)
    df = pd.read_html(StringIO(r.text))[0]
    df_dropped = df.droplevel(level=0, axis=1)
    df_dropped['date']= f'{years[i]}-{months[i]:02d}-{days[i]}'
    df_dropped.columns = new_columns
    currency_trade_list.append(df_dropped)
  except Exception as e:
    print(f"에러 발생: {e}")


# currency_trade_list[0]
for i in tqdm(range(len(currency_trade_list))):
  #currency_trade_list[i]= currency_trade_list[i].droplevel(level=0, axis=1)
  currency_trade_list[i].to_csv(f"./currency/{years[i]}-{months[i]:02d}-{days[i]}.csv", index=False, encoding = 'utf-8-sig')
