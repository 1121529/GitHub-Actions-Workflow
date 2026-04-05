import requests
import json
import datetime
import xml.dom.minidom  # 引入處理 XML 美化的模組

url = "https://api.nlsc.gov.tw/idc/ListRoadM/B/B01"

def main():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        content = response.text.strip()
        final_data = None

        # 1. 嘗試解析為 JSON
        try:
            final_data = response.json()
            print("解析成功：資料格式為 JSON")
        except json.JSONDecodeError:
            # 2. 如果 JSON 解析失敗，嘗試美化 XML
            print("非 JSON 格式，嘗試美化 XML...")
            try:
                # 使用 minidom 解析並重新生成帶縮排的字串
                dom = xml.dom.minidom.parseString(content)
                pretty_xml = dom.toprettyxml(indent="    ") # 設定 4 個空格縮排
                final_data = {"xml_content": pretty_xml}
                print("解析成功：資料格式為 XML (已完成美化排版)")
            except Exception as xml_err:
                print(f"XML 解析也失敗: {xml_err}")
                final_data = {"raw_content": content}

        # 3. 加入時間戳記
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output = {
            "update_time": current_time,
            "api_url": url,
            "data": final_data
        }
        
        # 4. 儲存檔案
        with open('road_data.json', 'w', encoding='utf-8') as f:
            # 這裡的 indent=4 是讓外層的 JSON 漂亮
            # 裡面的 XML 內容因為上面處理過，也會帶著 \n 與縮排
            json.dump(output, f, ensure_ascii=False, indent=4)
                
        print(f"檔案已儲存至 road_data.json")
        
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()
