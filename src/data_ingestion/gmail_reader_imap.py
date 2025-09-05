from imap_tools import MailBox
import os
from dotenv import load_dotenv

load_dotenv() 

def fetch_emails_imap(count=5):
    """Fetches emails using IMAP and an App Password."""
    user_email = os.getenv("GMAIL_EMAIL")
    user_password = os.getenv("GMAIL_APP_PASSWORD")

    if not user_email or not user_password:
        print("Error: Please set email/password in your .env file.")
        return []

    # Determine server based on email domain
    if 'outlook.com' in user_email or 'hotmail.com' in user_email:
        server = 'outlook.office365.com'
    else:
        server = 'imap.gmail.com'

    emails = []
    try:
        with MailBox(server).login(user_email, user_password, 'INBOX') as mailbox:
            for msg in mailbox.fetch(limit=count, reverse=True):
                emails.append({
                    "subject": msg.subject,
                    "from": msg.from_,
                    "body": msg.text or msg.html
                })
        print(f"Successfully fetched {len(emails)} emails from {server}.")
        return emails
    except Exception as e:
        print(f"An error occurred with IMAP: {e}")
        return []