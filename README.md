## 回測 IPO 上市股票的最佳投資持有時間：基於不同產業的研究 

### 研究方法概述 

> 本研究旨在通過程式化回測分析不同產業IPO股票的最佳持有期，以期找出持有期與最大收益之間的關聯。研究的整體流程如下： 

#### 系統架構 
- 使用語言為`python`，版本為`3.9+`，結合API應用並配合`Pandas`進行數據處理，再以`Matplotlib`進行數據可視化。
- 前置作業：準備公司清單等。
- 數據蒐集模組
  - 讀取IPO股票名單和股名字典。
  - 通過API接口從TWSE獲取與合併股票的歷史交易數據。(可處理多個月數據)
  - 處理上市日期的格式轉換。
- 資料前處理
- 報酬率計算模組
  - 主要IO格式為DataFrame。
  - 計算每日、每周、每月、每季度和半年報酬率。
  - 可將結果輸出為CSV文件。
- 產業分析模組
  - 主要IO格式為DataFrame。
  - 依產業別分組後，利用每日、每周、每月、每季度和半年報酬率計算標準差等統計資訊。
  - 具備結果可視化功能，更利於人類分析。
  - 可將結果輸出為CSV文件。

<div style="page-break-after: always;"></div>

#### 系統架構圖
![流程圖](https://github.com/user-attachments/assets/36e8d200-c5c7-4daa-9b14-27e9649e65fb)



#### 前置作業

1. 於證交所下載`ipo公司清單`，並將
   - `公司代號`標記為`symbol`
   - `上市日期`標記為`Listing date`
2. 儲存為`new_listing.csv`文件。
3. 製作股票代號及股票名稱對應的`code3.csv`文件，方便後續檢查。 

#### 數據蒐集

- 使用台灣證券交易所（TWSE）的API取得歷史交易數據，每次請求獲取一個月的數據，直到獲取到足夠的數據（例如180天的數據）。
1. 依據上市日期和股票代號，收集各IPO股票的日交易數據
   - 根據提供的`new_listing.csv`文件中的上市日期和股票代號進行數據收集。 
2. 將數據轉換為`DataFrame`型別，進行清洗和格式轉換。 

#### 資料前處理 
- 使用`Pandas`進行數據的異常值清理與標準化作業： 
  - 剔除無效或不完整的數值，確保後續作業結果正常。
  - 將民國年日期轉換為西元年日期，確保日期格式一致。

#### 報酬率計算
  - 計算上述數據資料的日、周、月、季以及半年報酬率作為回測結果。
  - 將回測結果輸出為CSV文件。 

<div style="page-break-after: always;"></div>

#### 產業分析：
  - 讀取報酬率CSV文件，並使用`Pandas`將其轉換為`DataFrame`進行處理。
  - 根據產業對數據進行分組計算，計算每個產業在不同持有期內的平均報酬率和標準差，並統計樣本數。

<div style="page-break-after: always;"></div>

#### 結果可視化： 

   - 使用`Matplotlib`繪製圖表，展示各產業在不同持有期內的平均報酬率及其標準差，可直觀分析結果。
   - 將統計結果輸出為新的`CSV`文件，便於後續的深入分析和報告撰寫。 

![a day_mean_std_sorted-1](https://github.com/user-attachments/assets/98823948-363e-4b15-b5b6-8b2146bdeb5a)
![a week_mean_std_sorted-1](https://github.com/user-attachments/assets/a7ac2c75-4dbe-49cb-b3e9-62afa5d66c47)
![a month_mean_std_sorted-1](https://github.com/user-attachments/assets/4bf33e33-d730-4d93-ad99-8d1c94918b3e)
![one season_mean_std_sorted-1](https://github.com/user-attachments/assets/b7c00197-a146-46e0-a5b1-7b75a2cc79eb)
![half a year_mean_std_sorted-1](https://github.com/user-attachments/assets/e31e3df1-fbf1-44e5-a0c0-e5cab048b6e5)



#### 結果分析

![表格數據](https://github.com/user-attachments/assets/e45f6e30-fe90-4dad-8058-427aa2596726)



 1. 總體概況： 我們對多個產業的IPO股票在不同持有期（當日、一週、一個月、一季、半年）內的平均報酬率及標準差進行了回測分析，以探討最佳投資持有時間。

 2. 行業表現分析：

- 半導體業

	- 一週平均報酬率最高，達到4.62%，但持有期延長至一季和半年後，報酬率分別下降至-1.92%和-8.36%，顯示出短期持有的優勢。

- 生技醫療業

  - 當日平均報酬率為3.54%，長期持有（一季和半年）的報酬率分別為10.75%和6.91%，此行業顯示出穩健的增長潛力。

- 光電業

  - 當日平均報酬率為0.46%，但長期持有顯示出顯著增長，一個月報酬率為4.55%，半年內則達到8.21%。

- 電子零組件業
  
  - 當日平均報酬率為5.70%，隨持有期延長，一季的平均報酬率達到9.58%，半年內可達15.21%，顯示出長期持有的價值。

- 汽車工業

  - 當日平均報酬率為負值，為-0.2%，但隨持有期延長，一個月的平均報酬率為4.27%，隨後下滑，顯示此行業具備短期增值空間。

- 電腦及週邊設備業

  - 當日報酬率約為4.88%，半年持有期報酬率提升至15.10%，顯示出較強的長期持有收益。

- 通信網路業

  - 當日平均報酬率為4.02%，隨持有期延長，一季時平均報酬率達34.66%，但標準差達146.58%，反映出該行業短期內具備一定的增值空間，但風險較高。

- 其他電子業

  - 當日平均報酬率為2.98%，一季時平均報酬率達8.85%，反映出該行業短期內具備一定的增值空間，但風險偏高。

- 航運業

  - 當日平均報酬率為0.71%，但一週報酬率轉為負值，半年的報酬率回升至5.92%，顯示出短期波動較大，長期收益尚可。

- 化學工業
	
  - 當日平均報酬率為1.71%，一週平均報酬率最高，達到5.53%，顯示該行業適合短期投資。

- 觀光餐旅業

  - 當日平均報酬率為15.31%，但半年持有期報酬率降至-8.41%，表明該行業適合短期投資而非長期持有。

- 電機機械/其他/綠能環保/貿易百貨/運動休閒
  - 當日平均報酬率分別為1.24%、0.4%、1.46%、-5.78%及-4.34%，後續無顯著亮點，顯示在選擇投資IPO時可考慮避開此類股票。

#### 結論
- 從本研究的回測結果可以得出以下結論：
  - 不同行業的IPO股票在不同持有期內的收益和風險顯著不同。
    - 日內操作：選擇觀光餐旅業的收益最佳，平均達15.31%。電子通路業和電子零組件業也有超過5%的平均收益。
    - 一周內：數位雲端業的平均收益最高，達14.49%。通信網路業、電子通路業和化學工業的平均收益也超過5%。
    - 月交易：通信網路業的平均收益最高，達23.38%。航運業也表現不錯，有10.52%的平均收益。
    - 季交易：通信網路業的平均收益最高，達34.66%。生技醫療業也有10.75%的不錯表現。雖然玻璃陶瓷業及資訊服務業的數據顯示10%以上的收益，但由於樣本數過少，未納入討論。
    - 半年交易：電子零組件業和電腦及週邊設備業的收益較好，平均達15%以上。紡織纖維、資訊服務業及食品工業的數據也顯示17%以上的收益，但樣本數過少，未納入討論。
  - 投資者應根據行業特性及市場情況調整投資持有期，以達到最佳收益。



#### 程式來源

https://github.com/MEME-K/meme-k/











