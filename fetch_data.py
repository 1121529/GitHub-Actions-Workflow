import requests
import json
import csv


url = "https://api.nlsc.gov.tw/other/MarkBufferAnlys/bus/120.634413/24.153282/70"

def main():
    try:
       
        response = requests.get(url)
        response.raise_for_status() 
        
        data = response.json()
        
        with open('library_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
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
