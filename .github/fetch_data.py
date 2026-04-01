import requests
import json
import csv

# 目標 API 網址 (教育部 106 學年度大專校院圖書館概況)
url = "https://stats.moe.gov.tw/files/opendata/106_25.json"

def main():
    try:
        # 發送 GET 請求
        response = requests.get(url)
        response.raise_for_status() # 檢查請求是否成功
        
        data = response.json()
        
        # 1. 儲存為 JSON 格式
        with open('library_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        # 2. 儲存為 CSV 格式 (取前幾項欄位作為範例)
        if len(data) > 0:
            keys = data[0].keys()
            with open('library_data.csv', 'w', newline='', encoding='utf-8-sig') as f:
                dict_writer = csv.DictWriter(f, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
                
        print("資料抓取與儲存成功！")
        
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()
