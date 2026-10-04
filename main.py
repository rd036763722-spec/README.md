import os
import json
import datetime
import urllib.request
import xml.etree.ElementTree as ET
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 1. איסוף חדשות מפיד RSS
def fetch_latest_news():
    rss_url = "https://www.maariv.co.il/Rss/RssFeedsMavzakim"  # דוגמה לפיד מבזקים
    req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        items = root.findall('./channel/item')
        
        news_list = []
        for item in items[:10]: # 10 המבזקים האחרונים
            title = item.find('title').text if item.find('title') is not None else ''
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
            news_list.append(f"• {title} ({pub_date})")
            
        return news_list
    except Exception as e:
        print(f"שגיאה באיסוף החדשות: {e}")
        return ["לא ניתן היה למשוך מבזקים כעת."]

# 2. יצירת קובץ הסיכום והעלאתו ל-Drive
def create_and_upload_summary():
    today_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"news_summary_{today_str}.txt"
    
    news = fetch_latest_news()
    
    # כתיבת התוכן לקובץ מקומי
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"=== סיכום חדשות יומי - {today_str} ===\n\n")
        for item in news:
            f.write(f"{item}\n\n")
            
    print(f"הקובץ {filename} נוצר בהצלחה. מעלה ל-Google Drive...")

    # התחברות ל-Google Drive
    creds_json = os.environ.get("GDRIVE_SERVICE_ACCOUNT")
    if not creds_json:
        print("שגיאה: חסר GDRIVE_SERVICE_ACCOUNT ב-Secrets")
        return

    info = json.loads(creds_json)
    scopes = ['https://www.googleapis.com/auth/drive.file']
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': filename}
    media = MediaFileUpload(filename, mimetype='text/plain')
    
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"הקובץ הועלה בהצלחה ל-Drive! מזהה: {uploaded_file.get('id')}")

if __name__ == "__main__":
    create_and_upload_summary()
