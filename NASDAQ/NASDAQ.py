import requests
import pandas as pd
from datetime import datetime
import os

now  =  datetime.now().strftime("%Y%m%d%H%M")

for file in os.listdir("/home/hadoop/workspace/NASDAQ/"):
    data = file.split(".")[0]
    url = f"https://api.stock.naver.com/chart/foreign/item/{data}.O/day?startDateTime=&endDateTime={now}"
    payload = {
    "endDateTime": f"{now}"
    }
    r = requests.get(url, data=payload)
    r_js = r.json()
    df = pd.DataFrame(r_js)
    df['code'] = data
    df['localDate'] = pd.to_datetime(df['localDate'], format='%Y%m%d')
    df.columns = ['date', 'close', 'open', 'high', 'low', 'volume', 'Symbol_Code']
    df.to_csv(f"/home/hadoop/workspace/today/{data}_{now}.csv",index=False,encoding="utf-8-sig")