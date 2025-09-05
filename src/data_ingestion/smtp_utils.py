# src/smtp_utils.py
import smtplib
from email.message import EmailMessage
from typing import Union, List, Tuple

def send_email_smtp(user_email: str, user_password: str,
                    to_emails: Union[str, List[str]],
                    subject: str, body: str, attachments: List[dict] = None,
                    timeout: int = 30) -> Tuple[bool, str]:
    """
    Send an email via SMTP. Returns (True, "OK") on success or (False, "Error message").
    attachments: list of dicts {'filename':..., 'content': bytes, 'maintype': 'application', 'subtype': 'pdf'}
    """
    to_list = to_emails if isinstance(to_emails, list) else [to_emails]

    # Detect provider for SMTP host/port
    lower = user_email.lower()
    if any(domain in lower for domain in ["outlook.com", "hotmail.com", "live.com"]):
        smtp_host = "smtp.office365.com"
        port = 587
        use_starttls = True
    elif any(domain in lower for domain in ["gmail.com", "googlemail.com"]):
        smtp_host = "smtp.gmail.com"
        port = 465
        use_starttls = False
    else:
        return False, "Unsupported email provider for SMTP."

    msg = EmailMessage()
    msg["From"] = user_email
    msg["To"] = ", ".join(to_list)
    msg["Subject"] = subject
    msg.set_content(body or "")

    if attachments:
        for att in attachments:
            content = att.get("content")
            filename = att.get("filename", "attachment")
            maintype = att.get("maintype", "application")
            subtype = att.get("subtype", "octet-stream")
            if content:
                msg.add_attachment(content, maintype=maintype, subtype=subtype, filename=filename)

    try:
        if use_starttls:
            with smtplib.SMTP(smtp_host, port, timeout=timeout) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(user_email, user_password)
                smtp.send_message(msg)
        else:
            with smtplib.SMTP_SSL(smtp_host, port, timeout=timeout) as smtp:
                smtp.login(user_email, user_password)
                smtp.send_message(msg)
        return True, "Email sent successfully."
    except Exception as e:
        return False, f"SMTP error: {e}"
