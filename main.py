
import os
import datetime
import urllib.request
import xml.etree.ElementTree as ET

def fetch_latest_news():
    # משיכת מבזקים מפיד RSS
    rss_url = "https://www.maariv.co.il/Rss/RssFeedsMavzakim"
    req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        items = root.findall('./channel/item')
        
        news_list = []
        for item in items[:10]:  # 10 המבזקים האחרונים
            title = item.find('title').text if item.find('title') is not None else ''
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
            news_list.append(f"- **{title}** ({pub_date})")
            
        return news_list
    except Exception as e:
        print(f"שגיאה באיסוף החדשות: {e}")
        return ["לא ניתן היה למשוך מבזקים כעת."]

def main():
    today_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    news = fetch_latest_news()
    
    # 1. יצירת תוכן הדו"ח
    content = f"# 📰 סיכום חדשות יומי - {today_str}\n\n"
    content += "\n".join(news)
    
    # 2. שמירת התוכן לקובץ במאגר
    filename = f"news_{today_str}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
        
    # 3. הדפסה ל-Summary של GitHub Actions (כדי שתראה את זה יפה ישר במסך)
    github_step_summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if github_step_summary:
        with open(github_step_summary, "a", encoding="utf-8") as f:
            f.write(content)

    print(f"הסיכום נשמר בהצלחה לקובץ {filename}!")

if __name__ == "__main__":
    main()
