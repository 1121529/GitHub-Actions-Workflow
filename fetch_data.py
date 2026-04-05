import requests
import json

url = "https://api.nlsc.gov.tw/idc/ListRoadM/B/B01"

def main():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        response = requests.get(url, headers=headers)
        
        
        if not response.text.strip():
            api_data = {"message": "伺服器回傳空值"}
        else:
            try:
                api_data = response.json()
            except json.JSONDecodeError:
                api_data = {"raw_content": response.text}
        
        output_data = {
            "api_url": url,
            "data": api_data
        }
        
        with open('road_data.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
                
        print(f"資料抓取成功")
        
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()
