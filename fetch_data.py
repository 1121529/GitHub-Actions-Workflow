import requests
import json
import datetime

# 新的目標 API 網址 (國土測繪中心 - 公車站環域分析)
url = "https://api.nlsc.gov.tw/other/MarkBufferAnlys/edu/120.634413/24.153282/100"

# ... 原本的程式碼 ...

def fetch_with_retry(url, max_retries=3):
    for i in range(max_retries):
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.text.strip(): # 如果內容不是空的
            return response.json()
        print(f"嘗試第 {i+1} 次抓取失敗，資料為空，等待後重試...")
        time.sleep(2) # 等待 2 秒再試
    return {"message": "多次嘗試後仍無資料"}
    
def main():
    try:
        # 加入 User-Agent，避免某些政府網站阻擋沒有瀏覽器標籤的爬蟲程式
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        # 發送 GET 請求
        response = requests.get(url, headers=headers)
        response.raise_for_status() # 檢查請求是否成功
        
        # 嘗試將回傳資料解析為 JSON
        # (有些政府 API 預設回傳 XML，這裡做個安全處理)
        try:
            api_data = response.json()
        except json.JSONDecodeError:
            print("注意：此 API 回傳的可能不是標準 JSON，將以純文字記錄")
            api_data = {"raw_content": response.text}

        # 💡 加入當前時間，確保每次執行產生的檔案內容都不一樣，Git 才會 Push！
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        output_data = {
            "update_time": current_time, # 記錄抓取時間
            "data": api_data             # 實際的 API 資料
        }
        
        # 儲存為 JSON 檔案 (檔名改為 bus_data.json)
        # 作業規定 JSON 或 CSV 擇一即可，因為這支 API 結構較深，存 JSON 最保險
        with open('bus_data.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
                
        print(f"資料抓取成功！已於 {current_time} 儲存為 bus_data.json")
        
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()
