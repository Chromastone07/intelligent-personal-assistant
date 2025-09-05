from imap_tools import MailBox

EMAIL = "okreport07@outlook.com"
PASS = "klydercyolemvbhb"

with MailBox("outlook.office365.com").login(EMAIL, PASS, "INBOX") as mailbox:
    for msg in mailbox.fetch(limit=3, reverse=True):
        print(msg.subject, msg.from_)
