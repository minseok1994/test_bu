# from selenium import webdriver
# import time
# import re
# import selenium
# print(selenium.__version__)
# from selenium.webdriver.chrome.service import Service
# CHROME_DRIVER_PATH = './chromedriver.exe'
# service = Service(executable_path=CHROME_DRIVER_PATH)
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(service=service, options=options)
# from selenium.webdriver.common.by import By
# driver.get("https://www.londonstockexchange.com/live-markets/market-data-dashboard/price-explorer?indices=UKX,MCX,NMX,ASX,AIM5,AIM1,AXX,FTSEORB,FTORBFG,FTORBNFG,FTORB5UG,FTORB5OG")
# time.sleep(10)
# driver.find_element(By.CSS_SELECTOR, "#onetrust-reject-all-handler").click()
# time.sleep(2)
# driver.find_element(By.CSS_SELECTOR, "#price-explorer > div:nth-child(7) > app-paginator > div > a:nth-child(3)").click()
# time.sleep(2)
# element= driver.find_element(By.CSS_SELECTOR, "#price-explorer-results-wrapper > tbody > tr:nth-child(1) > td.clickable.bold-font-weight.instrument-tidm.code.gtm-trackable.td-with-link > app-link-or-dash > a")
# element.text
# import timeit

# # 시간을 측정할 코드 블록
# code_block = """
# i=0
# if i < 2:
#     i= +1
# else:
#     i=2
# """

# # 코드 블록을 여러 번 실행하여 평균 실행 시간 측정
# execution_time = timeit.timeit(stmt=code_block, number=1000000)  # 예시로 100만 번 실행

# print(f"Average Execution Time: {execution_time:.10f} seconds")


# uk_stock_code = [0]

# #price-explorer > div:nth-child(7) > app-paginator > div > a:nth-child(3)
# #price-explorer > div:nth-child(7) > app-paginator > div > a:nth-child(4)
# #price-explorer > div:nth-child(7) > app-paginator > div > a:nth-child(5)
# #price-explorer > div:nth-child(7) > app-paginator > div > a:nth-child(4)
# # 계속 5를 반복
# # 전에 거와 같다면 6을 실행하고 종료한다 ㅇㅋ?

# page=[3,4,5,6]
# i=0
# while i < 3:
#     for y in range(1,20):
#         try:
#             element= driver.find_element(By.CSS_SELECTOR, f"#price-explorer-results-wrapper > tbody > tr:nth-child({y}) > td.clickable.bold-font-weight.instrument-tidm.code.gtm-trackable.td-with-link > app-link-or-dash > a")
#             if uk_stock_code[-1] == element.text:
#                 i=3
#                 time.sleep(2)
#                 print("하이")
#                 break
#             uk_stock_code.append(element.text)
#         except Exception as e:
#             print (e)
    
#     driver.find_element(By.CSS_SELECTOR, f"#price-explorer > div:nth-child(7) > app-paginator > div > a:nth-child({page[i]})").click()
#     if page[i] < 5:
#         i += 1
#     elif page[i] == 6:
#         for y in range(1,20):
#             try:
#                 element= driver.find_element(By.CSS_SELECTOR, f"#price-explorer-results-wrapper > tbody > tr:nth-child({y}) > td.clickable.bold-font-weight.instrument-tidm.code.gtm-trackable.td-with-link > app-link-or-dash > a")
#                 if uk_stock_code[-1] == element.text:
#                     i=3
#                     print("하이")
#                     break
#                 uk_stock_code.append(element.text)
#             except Exception as e:
#                 print (e)
#         print("종료직전")
#         break
#     time.sleep(2)


# uk_stock_code= list(set(uk_stock_code))
# del uk_stock_code[0]
# len(uk_stock_code)
# import pickle
# # 리스트를 파일에 저장
# with open('uk_stock_code.pkl', 'wb') as file:
#     pickle.dump(uk_stock_code, file)


import pickle
import os
from datetime import datetime, timedelta
import FinanceDataReader as fdr
from tqdm import tqdm

def load_stock_codes(file_path='uk_stock_code.pkl'):
    with open(file_path, 'rb') as file:
        loaded_list = pickle.load(file)
    return [s.replace('.', '') for s in loaded_list]

def fetch_and_save_stock_data(stock_code, start_date, end_date, output_dir='./uk_stock'):
    try:
        # FinanceDataReader를 사용하여 주식 정보 가져오기
        uk_stock = fdr.DataReader(stock_code, start_date, end_date)
        uk_stock.reset_index(inplace=True)
        uk_stock['Symbol_Code'] = stock_code

        # 파일 저장 경로 생성
        output_path = os.path.join(output_dir, f"{stock_code}.csv")

        # 주식 정보를 CSV 파일로 저장
        uk_stock.to_csv(output_path, index=False, encoding='utf-8-sig')
        
    except Exception as e:
        # 에러가 발생하면 에러 메시지 출력
        print(f"에러 발생: {e}")

def main():
    # 디렉토리가 없으면 생성
    output_directory = "./uk_stock"
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    # 오늘과 어제의 날짜 계산
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    # 주식 코드 로드
    modified_list = load_stock_codes()

    # 각 주식 코드에 대해 데이터 가져오기 및 저장
    for stock in tqdm(modified_list, desc="Fetching Stock Data"):
        stock_code = stock + '.L'
        start_date = '2000-01-01'
        end_date = today.strftime('%Y-%m-%d')  # 오늘까지의 데이터 가져오기

        fetch_and_save_stock_data(stock_code, start_date, end_date, output_directory)

if __name__ == "__main__":
    main()

