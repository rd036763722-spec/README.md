import os
import datetime
import urllib.request
import xml.etree.ElementTree as ET
import resend
from docx import Document

def get_news():
    url = "https://www.maariv.co.il/Rss/RssFeedsMavzakim"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    news = []
    try:
        with urllib.request.urlopen(req) as resp:
            root = ET.fromstring(resp.read())
            for item in root.findall('./channel/item')[:10]:
                title = item.find('title').text if item.find('title') is not None else ''
                news.append(title)
    except Exception as e:
        news.append("שגיאה באיסוף המבזקים.")
    return news

def main():
    today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    news_items = get_news()

    # יצירת מסמך Word בזיכרון
    doc = Document()
    doc.add_heading(f'סיכום חדשות - {today}', 0)
    for item in news_items:
        doc.add_paragraph(item, style='List Bullet')
    
    doc_filename = f"News_Summary_{today}.docx"
    doc.save(doc_filename)

    # שליחה דרך Resend
    api_key = os.environ.get("RESEND_API_KEY")
    recipient_email = os.environ.get("RECIPIENT_EMAIL")

    if api_key and recipient_email:
        resend.api_key = api_key

        with open(doc_filename, "rb") as f:
            file_bytes = list(f.read())

        params = {
            "from": "onboarding@resend.dev",
            "to": [recipient_email],
            "subject": f"סיכום חדשות יומי - {today}",
            "html": "<p>שלום,<br>מצורף קובץ ה-Word עם סיכום החדשות היומי.</p>",
            "attachments": [
                {
                    "filename": doc_filename,
                    "content": file_bytes,
                }
            ]
        }

        email_response = resend.Emails.send(params)
        print("המייל נשלח בהצלחה!", email_response)
    else:
        print("שגיאה: חסרים משתני סביבה (RESEND_API_KEY / RECIPIENT_EMAIL)")

if __name__ == "__main__":
    main()
