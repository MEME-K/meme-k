# 吃TWSE資料，需調整股名和上市日期2010/7/20前可能需注意數據位置
# 可批量處理，需吃"new_listing" 和"code3.csv"
import pandas as pd
import requests
from datetime import datetime, timedelta
import csv

# 將民國年日期轉換為西元年日期的函數
def convert_roc_to_ad(roc_date):
    try:
        parts = roc_date.split('.')
        year = int(parts[0]) + 1911
        month = int(parts[1])
        day = int(parts[2])
        return datetime(year, month, day)
    except (ValueError, IndexError):
        return None

# 計算報酬率的函數
def calculate_return(open_price, close_price):
    return (close_price - open_price) / open_price * 100

# 讀取股名字典
code3 = {}
with open(r'D:\魚魚\小群資料\新增資料夾\個股2\code3.csv', newline='', encoding='utf-8') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        code3[row[0]] = row[1]

# 讀取 new_listing.csv 文件
new_listing_df = pd.read_csv(r'D:\Python\python 澎澎\試作IPO回測\new_listing.csv', encoding='utf-8')

# 將日期欄位轉換為字串，並處理空值和無效值
new_listing_df['Listing date'] = new_listing_df['Listing date'].astype(str).fillna('')

# 初始化結果列表
results = []

# 遍歷每一行數據
for index, row in new_listing_df.iterrows():
    stock_code = row['symbol']
    roc_listing_date = row['Listing date']
    
    # 跳過空的或無效的日期欄位
    if not roc_listing_date or roc_listing_date.lower() == 'nan':
        continue
    
    # 將民國年日期轉換為西元年日期
    listing_date = convert_roc_to_ad(roc_listing_date)
    if not listing_date:
        continue
    
    # 查詢股名
    stock_name = code3.get(str(stock_code), "未知股票")
    
    # 初始化 DataFrame
    all_data = pd.DataFrame()

    # 獲取多個月的數據
    current_date = listing_date
    while len(all_data) < 180:
        start_date = current_date.strftime('%Y%m%d')
        api_url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={start_date}&stockNo={stock_code}"
        response = requests.get(api_url)

        # 檢查 API 請求是否成功
        if response.status_code != 200:
            print("無法獲取數據，請檢查股票代號和日期是否正確。")
            break

        # 檢查返回的內容是否為有效的 JSON
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("返回的數據不是有效的 JSON 格式。")
            break

        # 檢查數據是否包含 'data' 和 'fields' 欄位
        if 'data' not in data or 'fields' not in data:
            print(f"數據中缺少必要的欄位，股票代號: {stock_code}")
            break

        # 將數據轉換為 DataFrame 並追加到 all_data
        df = pd.DataFrame(data['data'], columns=data['fields'])
        all_data = pd.concat([all_data, df], ignore_index=True)

        # 更新 current_date 為下一個月
        current_date += timedelta(days=30)

    # 確保有足夠的數據進行計算
    if len(all_data) < 127:
        continue

    # 處理開盤價和收盤價
    try:
        open_price = float(all_data.iloc[0][3])  # 假設開盤價在第4列
        close_price = float(all_data.iloc[0][6])  # 假設收盤價在第7列
    except ValueError:
        print(f"無法轉換開盤價或收盤價為浮點數，股票代號: {stock_code}")
        continue

    # 報酬率計算
    returns = {
        "當日報酬率": close_price - open_price,
        "一周報酬率": calculate_return(open_price, float(all_data.iloc[4][6])) if len(all_data) > 4 else None,
        "一個月報酬率": calculate_return(open_price, float(all_data.iloc[20][6])) if len(all_data) > 20 else None,
        "三個月報酬率": calculate_return(open_price, float(all_data.iloc[60][6])) if len(all_data) > 60 else None,
        "半年報酬率": calculate_return(open_price, float(all_data.iloc[120][6])) if len(all_data) > 120 else None,
    }
    
    # 將結果添加到列表中
    results.append({
        "股票代號": stock_code,
        "股名": stock_name,
        "上市日期": listing_date.strftime('%Y-%m-%d'),
        "當日報酬日期": listing_date.strftime('%Y-%m-%d'),
        "當日開盤價": open_price,
        "當日收盤價": close_price,
        "當日報酬率": returns["當日報酬率"],
        "一周報酬率": returns["一周報酬率"],
        "一個月報酬率": returns["一個月報酬率"],
        "三個月報酬率": returns["三個月報酬率"],
        "半年報酬率": returns["半年報酬率"],
    })

# 將結果轉換為 DataFrame
output_df = pd.DataFrame(results)

# 將結果保存為 CSV 文件
output_path = r'D:\Python\python 澎澎\試作IPO回測\ipo_results.csv'
output_df.to_csv(output_path, index=False, encoding='utf-8-sig')


# 顯示前兩筆數據結果
print("前兩筆數據結果:")
for i in range(min(2, len(results))):
    result = results[i]
    print(f"股票代號: {result['股票代號']}")
    print(f"股票名稱: {result['股名']}")
    print(f"上市日期: {result['上市日期']}")
    print(f"當日報酬日期: {result['當日報酬日期']}")
    print(f"當日開盤價: {result['當日開盤價']}")
    print(f"當日收盤價: {result['當日收盤價']}")
    print(f"當日報酬率: {result['當日報酬率']:.2f}%")
    if result["一周報酬率"] is not None:
        one_week_date = datetime.strptime(result['上市日期'], '%Y-%m-%d') + timedelta(days=5)
        one_week_close_price = float(all_data.iloc[4][6])
        print(f"一周報酬日期: {one_week_date.strftime('%Y-%m-%d')}")
        print(f"一周開盤價: {result['當日開盤價']}")
        print(f"一周收盤價: {one_week_close_price}")
        print(f"一周報酬率: {result['一周報酬率']:.2f}%")
    if result["一個月報酬率"] is not None:
        one_month_date = datetime.strptime(result['上市日期'], '%Y-%m-%d') + timedelta(days=21)
        one_month_close_price = float(all_data.iloc[20][6])
        print(f"一個月報酬日期: {one_month_date.strftime('%Y-%m-%d')}")
        print(f"一個月開盤價: {result['當日開盤價']}")
        print(f"一個月收盤價: {one_month_close_price}")
        print(f"一個月報酬率: {result['一個月報酬率']:.2f}%")
    if result["三個月報酬率"] is not None:
        three_month_date = datetime.strptime(result['上市日期'], '%Y-%m-%d') + timedelta(days=63)
        three_month_close_price = float(all_data.iloc[60][6])
        print(f"三個月報酬日期: {three_month_date.strftime('%Y-%m-%d')}")
        print(f"三個月開盤價: {result['當日開盤價']}")
        print(f"三個月收盤價: {three_month_close_price}")
        print(f"三個月報酬率: {result['三個月報酬率']:.2f}%")
    if result["半年報酬率"] is not None:
        six_month_date = datetime.strptime(result['上市日期'], '%Y-%m-%d') + timedelta(days=126)
        six_month_close_price = float(all_data.iloc[120][6])
        print(f"半年報酬日期: {six_month_date.strftime('%Y-%m-%d')}")
        print(f"半年開盤價: {result['當日開盤價']}")
        print(f"半年收盤價: {six_month_close_price}")
        print(f"半年報酬率: {result['半年報酬率']:.2f}%")

print(f"結果已保存到 {output_path}")
