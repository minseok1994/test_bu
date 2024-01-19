import pandas as pd
import os
import datetime
import FinanceDataReader as fdr

def fetch_daily_data(symbol, date):
    try:
        symbol_with_exchange = 'SSE:' + symbol
        # 해당 날짜의 데이터를 불러옵니다.
        df = fdr.DataReader(symbol_with_exchange, start=date, end=date)

        if not df.empty:
            # 컬럼 순서 변경 및 Symbol_Code 컬럼 추가
            df = df.reset_index()
            df['Symbol_Code'] = symbol
            df = df[['Date', 'Close', 'Open', 'High', 'Low', 'Volume', 'Symbol_Code']]

            # 파일 저장 경로 설정
            directory_path = f'./stock/'
            os.makedirs(directory_path, exist_ok=True)
            file_path = os.path.join(directory_path, f"{symbol}_{current_date}.csv")

            # CSV 파일로 저장
            df.to_csv(file_path, index=False)

            return symbol

    except Exception as e:
        print(f"Error occurred for {symbol}: {e}")
        return None

# 상해 상장종목 전체 목록
df_sse = fdr.StockListing('SSE')
list_sse = df_sse['Symbol']

def main():
    # 현재 날짜 가져오기
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # 각 종목에 대해 데이터 수집
    for symbol in list_sse:
        fetch_daily_data(symbol, current_date)

if __name__ == "__main__":
    main()

