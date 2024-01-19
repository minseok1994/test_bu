import requests
import pandas as pd
import os
from datetime import datetime, timedelta
from tqdm import tqdm

def make_directory(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)

def format_date(date):
    return datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')

def get_stock_data(ticker, start_date, end_date):
    url = f"https://api.finance.naver.com/siseJson.naver?symbol={ticker}&requestType=2&count=1&startTime={start_date}&timeframe=day"
    r = requests.post(url)
    df = pd.DataFrame(eval(r.text.strip())[1:], columns=eval(r.text.strip())[0])
    df['ticker'] = ticker
    df['name'] = code_dict[ticker]
    df.dropna(inplace=True)
    df.columns = new_columns
    df['date'] = df['date'].apply(format_date)
    return df

def download_stock_data(directory, tickers, start_date, end_date):
    for ticker in tqdm(tickers):
        url = f"https://api.finance.naver.com/siseJson.naver?symbol={ticker}&requestType=2&count=1&startTime={end_date}&timeframe=day"
        r = requests.post(url)
        df1 = pd.DataFrame(eval(r.text.strip())[1:], columns=eval(r.text.strip())[0])

        url = f"https://api.finance.naver.com/siseJson.naver?symbol={ticker}&requestType=2&count=1&startTime={start_date}&timeframe=day"
        r = requests.post(url)
        df2 = pd.DataFrame(eval(r.text.strip())[1:], columns=eval(r.text.strip())[0])

        if (df1['날짜'] != df2['날짜']).values:
            df = get_stock_data(ticker, start_date, end_date)
            df.to_csv(f"{directory}/{ticker}_{end_date}.csv", index=False, encoding='utf-8-sig')
        break

if __name__ == "__main__":
    today = datetime.now().strftime('%Y%m%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

    make_directory("./kospi")

    # 주식 코드 가져오기
    url2 = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    payload2 = {
        "bld": "dbms/MDC/STAT/standard/MDCSTAT01901",
        "locale": "ko_KR",
        "mktId": "ALL",
        "share": "1",
        "csvxls_isNo": "false",
    }
    r2 = requests.post(url2, data=payload2)
    dict_pd = pd.DataFrame(r2.json()['OutBlock_1'])[['ISU_SRT_CD', 'ISU_ABBRV']]

    dict_pd.set_index('ISU_SRT_CD', inplace=True)
    code_dict = dict_pd.to_dict()['ISU_ABBRV']

    new_columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'forign_rate', 'Symbol_Code', 'name']

    download_stock_data("./kospi", code_dict.keys(), yesterday, today)
