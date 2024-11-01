# # 可批量處理，圖輸出自大到小
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib import font_manager

# # 設定字體
# font_path = 'C:/Windows/Fonts/msjh.ttc'  # 請確認這裡的字體路徑是否正確
# font_prop = font_manager.FontProperties(fname=font_path)

# # 讀取 CSV 檔案，指定完整路徑和編碼
# file_path = 'D:/Python/python 澎澎/試作IPO回測/ipo_results 2.csv'
# df = pd.read_csv(file_path, encoding='utf-8')

# # 指定要計算的欄位
# columns_to_analyze = ['a day', 'a week', 'a month', 'one season', 'half a year']

# # 分組計算
# grouped = df.groupby('industry')

# # 創建一個空的 DataFrame 來存儲結果
# result_df = pd.DataFrame()

# # 對每個群組進行計算並添加到結果 DataFrame
# for name, group in grouped:
#     means = group[columns_to_analyze].mean()
#     stds = group[columns_to_analyze].std()
#     counts = group[columns_to_analyze].count()
    
#     # 添加群組名稱
#     group.loc['mean'] = means
#     group.loc['std'] = stds
#     group.loc['count'] = counts
#     group['industry'] = name
    
#     # 將結果添加到結果 DataFrame
#     result_df = pd.concat([result_df, group])

# # 創建一個新的 DataFrame 來存儲每個 industry 的統計數據
# summary_df = pd.DataFrame(columns=[
#     'Industry', 'a day的平均值', 'a day的標準差', 'a day的樣本數',
#     'a week的平均值', 'a week的標準差', 'a week的樣本數',
#     'a month的平均值', 'a month的標準差', 'a month的樣本數',
#     'one season的平均值', 'one season的標準差', 'one season的樣本數',
#     'half a year的平均值', 'half a year的標準差', 'half a year的樣本數'
# ])

# # 對每個群組計算統計數據並添加到 summary_df
# for name, group in grouped:
#     summary_data = {
#         'Industry': name,
#         'a day的平均值': group['a day'].mean(),
#         'a day的標準差': group['a day'].std(),
#         'a day的樣本數': group['a day'].count(),
#         'a week的平均值': group['a week'].mean(),
#         'a week的標準差': group['a week'].std(),
#         'a week的樣本數': group['a week'].count(),
#         'a month的平均值': group['a month'].mean(),
#         'a month的標準差': group['a month'].std(),
#         'a month的樣本數': group['a month'].count(),
#         'one season的平均值': group['one season'].mean(),
#         'one season的標準差': group['one season'].std(),
#         'one season的樣本數': group['one season'].count(),
#         'half a year的平均值': group['half a year'].mean(),
#         'half a year的標準差': group['half a year'].std(),
#         'half a year的樣本數': group['half a year'].count()
#     }
#     summary_df = pd.concat([summary_df, pd.DataFrame([summary_data])], ignore_index=True)

# # 按照各時間段的平均值從大到小排列
# for period in columns_to_analyze:
#     summary_df = summary_df.sort_values(by=f'{period}的平均值', ascending=False)

#     # 繪製並儲存圖表
#     plt.figure(figsize=(10, 6))
#     plt.errorbar(summary_df['Industry'], summary_df[f'{period}的平均值'], yerr=summary_df[f'{period}的標準差'], fmt='o', capsize=5)
#     plt.title(f'{period}的平均值和標準差', fontproperties=font_prop)
#     plt.xlabel('Industry', fontproperties=font_prop)
#     plt.ylabel(f'{period}的平均值', fontproperties=font_prop)
#     plt.xticks(rotation=45, ha='right', fontproperties=font_prop)
#     plt.grid(True)
#     plt.tight_layout()
#     plt.savefig(f'D:/Python/python 澎澎/試作IPO回測/{period}_mean_std_sorted.png')
#     plt.close()

# # 輸出新的 summary CSV 檔案，指定編碼
# summary_output_path = 'D:/Python/python 澎澎/試作IPO回測/ipo_analyze_2.csv'
# summary_df.to_csv(summary_output_path, encoding='utf-8-sig', index=False)

# print("分析結果已儲存到 'ipo_analyze_2.csv'")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

# 設定字體
font_path = 'C:/Windows/Fonts/msjh.ttc'  # 請確認這裡的字體路徑是否正確
font_prop = font_manager.FontProperties(fname=font_path)

# 讀取 CSV 檔案，指定完整路徑和編碼
file_path = 'D:/Python/python 澎澎/試作IPO回測/ipo_results 2.csv'
df = pd.read_csv(file_path, encoding='utf-8')

# 指定要計算的欄位
columns_to_analyze = ['a day', 'a week', 'a month', 'one season', 'half a year']
columns_to_analyze_zh = ['日報酬', '周報酬', '月報酬', '季報酬', '半年報酬']

# 分組計算
grouped = df.groupby('industry')

# 創建一個空的 DataFrame 來存儲結果
result_df = pd.DataFrame()

# 對每個群組進行計算並添加到結果 DataFrame
for name, group in grouped:
    means = group[columns_to_analyze].mean()
    stds = group[columns_to_analyze].std()
    counts = group[columns_to_analyze].count()
    
    # 添加群組名稱
    group.loc['mean'] = means
    group.loc['std'] = stds
    group.loc['count'] = counts
    group['industry'] = name
    
    # 將結果添加到結果 DataFrame
    result_df = pd.concat([result_df, group])

# 創建一個新的 DataFrame 來存儲每個 industry 的統計數據
summary_df = pd.DataFrame(columns=[
    'Industry', 'a day的平均值', 'a day的標準差', 'a day的樣本數',
    'a week的平均值', 'a week的標準差', 'a week的樣本數',
    'a month的平均值', 'a month的標準差', 'a month的樣本數',
    'one season的平均值', 'one season的標準差', 'one season的樣本數',
    'half a year的平均值', 'half a year的標準差', 'half a year的樣本數'
])

# 對每個群組計算統計數據並添加到 summary_df
for name, group in grouped:
    summary_data = {
        'Industry': name,
        'a day的平均值': group['a day'].mean(),
        'a day的標準差': group['a day'].std(),
        'a day的樣本數': group['a day'].count(),
        'a week的平均值': group['a week'].mean(),
        'a week的標準差': group['a week'].std(),
        'a week的樣本數': group['a week'].count(),
        'a month的平均值': group['a month'].mean(),
        'a month的標準差': group['a month'].std(),
        'a month的樣本數': group['a month'].count(),
        'one season的平均值': group['one season'].mean(),
        'one season的標準差': group['one season'].std(),
        'one season的樣本數': group['one season'].count(),
        'half a year的平均值': group['half a year'].mean(),
        'half a year的標準差': group['half a year'].std(),
        'half a year的樣本數': group['half a year'].count()
    }
    summary_df = pd.concat([summary_df, pd.DataFrame([summary_data])], ignore_index=True)

# 按照各時間段的平均值從大到小排列並繪製圖表
for period, period_zh in zip(columns_to_analyze, columns_to_analyze_zh):
    summary_df = summary_df.sort_values(by=f'{period}的平均值', ascending=False)

    # 自訂標題
    custom_title = f'{period_zh}的平均值和標準差'

    plt.figure(figsize=(10, 6))
    plt.errorbar(summary_df['Industry'], summary_df[f'{period}的平均值'], yerr=summary_df[f'{period}的標準差'], fmt='o', capsize=5)
    plt.title(custom_title, fontproperties=font_prop)  # 這裡設定標題
    plt.xlabel('Industry', fontproperties=font_prop)
    plt.ylabel(f'{period_zh}的平均值', fontproperties=font_prop)
    plt.xticks(rotation=45, ha='right', fontproperties=font_prop)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'D:/Python/python 澎澎/試作IPO回測/{period}_mean_std_sorted.png')
    plt.close()

# 輸出新的 summary CSV 檔案，指定編碼
summary_output_path = 'D:/Python/python 澎澎/試作IPO回測/ipo_analyze_2.csv'
summary_df.to_csv(summary_output_path, encoding='utf-8-sig', index=False)

print("分析結果已儲存到 'ipo_analyze_2.csv'")
