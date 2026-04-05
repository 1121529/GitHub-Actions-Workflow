import requests
import json
import datetime

url = "https://api.nlsc.gov.tw/other/MarkBufferAnlys/bus/120.634413/24.153282/70"

def main():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        try:
            api_data = response.json()
        except json.JSONDecodeError:
            api_data = {"raw_content": response.text}

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        output_data = {
            "update_time": current_time, 
            "data": api_data            
        }
        
        with open('bus_data.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
                
        print(f"資料抓取成功")
        
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()
