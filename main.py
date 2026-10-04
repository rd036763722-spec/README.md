import os
import datetime
import smtplib
import urllib.request
import xml.etree.ElementTree as ET
from email.message import EmailMessage
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

    # יצירת המסמך
    doc = Document()
    doc.add_heading(f'סיכום חדשות - {today}', 0)
    for item in news_items:
        doc.add_paragraph(item, style='List Bullet')
    
    doc_filename = f"News_Summary_{today}.docx"
    doc.save(doc_filename)

    # שליחת המייל עם הקובץ המצורף
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASS")
    recipient_email = os.environ.get("RECIPIENT_EMAIL")

    if sender_email and sender_password and recipient_email:
        msg = EmailMessage()
        msg['Subject'] = f"סיכום חדשות יומי - {today}"
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg.set_content("שלום,\n\nמצורף סיכום החדשות היומי בקובץ Word.\nתוכל לחץ על האייקון של Google Drive בג'ימייל כדי לשמור אותו ישירות לדרייב שלך!")

        with open(doc_filename, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(
                file_data,
                maintype='application',
                subtype='vnd.openxmlformats-officedocument.wordprocessingml.document',
                filename=doc_filename
            )

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("המייל נשלח בהצלחה!")

if __name__ == "__main__":
    main()
