import requests
import json
import datetime

# 新的目標 API 網址 (國土測繪中心 - 道路名稱查詢)
url = "https://api.nlsc.gov.tw/idc/ListRoadM/B/B01"

def main():
    try:
        # 加入 User-Agent 偽裝成瀏覽器，避免被政府網站阻擋
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        # 發送 GET 請求
        response = requests.get(url, headers=headers)
        
        # 列印狀態碼方便你在 GitHub Actions 裡除錯 (200 代表成功)
        print(f"API 伺服器回應狀態碼: {response.status_code}")
        response.raise_for_status() 
        
        # 檢查伺服器回傳內容是否為空
        if not response.text.strip():
            api_data = {"message": "伺服器回傳空值"}
        else:
            # 嘗試將回傳資料解析為 JSON；如果政府 API 給的是 XML，則存為文字
            try:
                api_data = response.json()
            except json.JSONDecodeError:
                print("注意：此 API 回傳的不是標準 JSON (可能是 XML)，將以純文字記錄")
                api_data = {"raw_content": response.text}

        # 加入當前時間，確保每次執行產生的檔案內容都有變動，Git 才會執行 Push
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        output_data = {
            "update_time": current_time,
            "api_url": url,
            "data": api_data
        }
        
        # 儲存為 JSON 檔案 (檔名改為 road_data.json)
        with open('road_data.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
                
        print(f"資料抓取成功！已於 {current_time} 儲存為 road_data.json")
        
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()
