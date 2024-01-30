import pandas as pd
import requests
import json
from datetime import datetime
from tqdm import tqdm
import subprocess

HADOOP_HOME = "/home/hadoop/hadoop"
HDFS_PATH = "/stock/TYO"
LOCAL_DATA_PATH = "/home/hadoop/today_update"

def fetch_japan_stocks(url):
    all_data = []

    page = 1
    while True:
        payload = {
            "page": str(page),
            "pageSize": "20"
        }
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            data = response.json().get('stocks', [])
            all_data.extend(data)

            if len(data) == 0:
                break
            else:
                page += 1
        else:
            print(f'HTTP 요청 실패: {response.status_code}')
            break

    return pd.DataFrame(all_data)

def fetch_and_save_data(symbol_codes, output_folder='today_update'):
    current_date_str = datetime.now().strftime('%Y%m%d')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for symbol in tqdm(symbol_codes, desc="Fetching Data"):
        url = f"https://api.stock.naver.com/chart/foreign/item/{symbol}.T/day?startDateTime={current_date_str}0000&endDateTime={current_date_str}2359"
        response = requests.get(url).text
        data = json.loads(response)