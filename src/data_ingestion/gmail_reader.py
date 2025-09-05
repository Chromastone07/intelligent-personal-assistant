# from turtle import st
# from imap_tools import MailBox
# import os
# from dotenv import load_dotenv

# load_dotenv() 

# def fetch_emails_imap(count=5):
#     """Fetches emails using IMAP and an App Password."""
#     user_email = os.getenv("GMAIL_EMAIL")
#     user_password = os.getenv("GMAIL_APP_PASSWORD")

#     if not user_email or not user_password:
#         print("Error: Please set email/password in your .env file.")
#         return []

#     # Determine server based on email domain
#     if any(domain in user_email for domain in ["outlook.com", "hotmail.com", "live.com"]):
#      server = "outlook.office365.com"
#     elif any(domain in user_email for domain in ["gmail.com", "googlemail.com"]):
#      server = "imap.gmail.com"
#     else:
#      st.error("Unsupported email provider. Please use Gmail or Outlook/Hotmail.")
#      st.stop()


#     emails = []
#     try:
#         with MailBox(server).login(user_email, user_password, 'INBOX') as mailbox:
#             for msg in mailbox.fetch(limit=count, reverse=True):
#                 emails.append({
#                     "subject": msg.subject,
#                     "from": msg.from_,
#                     "body": msg.text or msg.html
#                 })
#         print(f"Successfully fetched {len(emails)} emails from {server}.")
#         return emails
#     except Exception as e:
#         print(f"An error occurred with IMAP: {e}")
#         return []








# import os
# from imap_tools import MailBox, AND
# from dotenv import load_dotenv
# from src.data_ingestion.document_parser import parse_pdf, parse_txt

# load_dotenv()

# def fetch_emails_imap(count=5, folder="INBOX"):
#     """
#     Fetches latest emails via IMAP (supports Gmail/Outlook).
#     Also extracts text from PDF/TXT attachments.
#     """
#     user_email = os.getenv("GMAIL_EMAIL")
#     user_password = os.getenv("GMAIL_APP_PASSWORD")

#     if not user_email or not user_password:
#         print("❌ Please set GMAIL_EMAIL and GMAIL_APP_PASSWORD in your .env file.")
#         return []

#     # Pick IMAP server
#     if any(domain in user_email for domain in ["outlook.com", "hotmail.com", "live.com"]):
#         server = "outlook.office365.com"
#     elif any(domain in user_email for domain in ["gmail.com", "googlemail.com"]):
#         server = "imap.gmail.com"
#     else:
#         raise ValueError("Unsupported provider: Only Gmail & Outlook supported.")

#     emails = []
#     try:
#         with MailBox(server).login(user_email, user_password, folder) as mailbox:
#             for msg in mailbox.fetch(criteria=AND(all=True), limit=count, reverse=True):
#                 email_data = {
#                     "subject": msg.subject,
#                     "from": msg.from_,
#                     "date": msg.date_str,
#                     "body": msg.text or msg.html or "",
#                     "attachments": []
#                 }

#                 # Process attachments
#                 for att in msg.attachments:
#                     att_text = None
#                     if att.filename.lower().endswith(".pdf"):
#                         att_text = parse_pdf(att.payload)
#                     elif att.filename.lower().endswith(".txt"):
#                         att_text = parse_txt(att.payload)

#                     if att_text:
#                         email_data["attachments"].append({
#                             "filename": att.filename,
#                             "content": att_text
#                         })

#                 emails.append(email_data)

#         print(f"✅ Successfully fetched {len(emails)} emails from {server}.")
#         return emails

#     except Exception as e:
#         print(f"❌ IMAP error: {e}")
#         return []











# from imap_tools import MailBox

# def fetch_emails_imap(count=5, user_email=None, user_password=None):
#     """Fetches emails using IMAP and App Password (Gmail or Outlook)."""
#     if not user_email or not user_password:
#         print("Error: Missing email or password.")
#         return []

#     # Determine IMAP server
#     if any(domain in user_email for domain in ["outlook.com", "hotmail.com", "live.com"]):
#         server = "outlook.office365.com"
#     elif any(domain in user_email for domain in ["gmail.com", "googlemail.com"]):
#         server = "imap.gmail.com"
#     else:
#         print("Unsupported provider. Use Gmail or Outlook.")
#         return []

#     emails = []
#     try:
#         with MailBox(server).login(user_email, user_password, "INBOX") as mailbox:
#             for msg in mailbox.fetch(limit=count, reverse=True):
#                 emails.append({
#                     "subject": msg.subject,
#                     "from": msg.from_,
#                     "body": msg.text or msg.html
#                 })
#         print(f"✅ Successfully fetched {len(emails)} emails from {server}.")
#         return emails
#     except Exception as e:
#         print(f"❌ IMAP Error: {e}")
#         return []









# src/gmail_reader.py
# from imap_tools import MailBox
# from typing import List, Dict

# def fetch_emails_imap(user_email: str, user_password: str, count: int = 5, folder: str = "INBOX") -> List[Dict]:
#     """
#     Fetch emails using IMAP with given credentials.
#     Returns list of dicts: {subject, from, date, body, attachments: [{filename, content_bytes}, ...]}
#     Raises Exception with descriptive message on failure.
#     """
#     if not user_email or not user_password:
#         raise ValueError("Missing Gmail address or app password.")

#     # choose IMAP server
#     if any(domain in user_email.lower() for domain in ["outlook.com", "hotmail.com", "live.com"]):
#         server = "outlook.office365.com"
#     elif any(domain in user_email.lower() for domain in ["gmail.com", "googlemail.com"]):
#         server = "imap.gmail.com"
#     else:
#         raise ValueError("Unsupported email provider (use Gmail or Outlook/Hotmail).")

#     emails = []
#     try:
#         # login; imap_tools: MailBox(server).login(user, password, folder)
#         with MailBox(server).login(user_email, user_password, folder) as mailbox:
#             for msg in mailbox.fetch(limit=count, reverse=True):
#                 body = msg.text or msg.html or ""
#                 attachments = []
#                 for att in msg.attachments:
#                     try:
#                         attachments.append({
#                             "filename": att.filename,
#                             "content": att.payload  # raw bytes
#                         })
#                     except Exception:
#                         # fallback
#                         attachments.append({"filename": getattr(att, "filename", "attachment"), "content": None})
#                 emails.append({
#                     "subject": msg.subject or "(no subject)",
#                     "from": msg.from_,
#                     "date": getattr(msg, "date_str", str(getattr(msg, "date", ""))),
#                     "body": body,
#                     "attachments": attachments
#                 })
#         return emails
#     except Exception as e:
#         # Provide helpful info to UI
#         raise Exception(f"IMAP connection error to {server}: {e}")




from imap_tools import MailBox, AND

def fetch_emails_imap(user_email: str, user_password: str, count: int = 5, folder: str = "INBOX"):
    """
    Fetches emails using IMAP and an App Password.
    Returns list of dicts {subject, from, date, body, attachments: [...] }.
    """
    if not user_email or not user_password:
        raise ValueError("Missing email or app password")

    # Pick server based on domain
    if any(domain in user_email for domain in ["outlook.com", "hotmail.com", "live.com"]):
        server = "outlook.office365.com"
    elif any(domain in user_email for domain in ["gmail.com", "googlemail.com"]):
        server = "imap.gmail.com"
    else:
        raise ValueError("Unsupported email provider. Please use Gmail or Outlook/Hotmail.")

    emails = []
    try:
        with MailBox(server).login(user_email, user_password, folder) as mailbox:
            for msg in mailbox.fetch(criteria=AND(all=True), limit=count, reverse=True):
                email_data = {
                    "subject": msg.subject,
                    "from": msg.from_,
                    "date": msg.date,
                    "body": msg.text or msg.html,
                    "attachments": []
                }
                for att in msg.attachments:
                    email_data["attachments"].append({
                        "filename": att.filename,
                        "content": att.payload.decode(errors="ignore") if att.is_inline else None
                    })
                emails.append(email_data)
        return emails
    except Exception as e:
        print(f"[IMAP ERROR] {e}")
        return []
