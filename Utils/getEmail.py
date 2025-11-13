import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

# Loading .env secrets
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
load_dotenv(env_path)

# IMAP server settings
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993  # Standard IMAP SSL port

# Your email credentials
EMAIL_ADDRESS = os.getenv("GMAIL_ADDR")
EMAIL_PASSWORD = os.getenv("GMAIL_PASS")

# Connect to the IMAP server
imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

# Log in to your email account
imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

# Select the mailbox you want to watch (e.g., "INBOX")
mailbox = "INBOX"
imap.select(mailbox)

# Continuously check for new messages
while True:
    # Search for all unseen messages
    status, message_ids = imap.search(None, "UNSEEN")

    if status == "OK":
        message_ids = message_ids[0].split()
        for message_id in message_ids:
            # Fetch the email message
            status, message_data = imap.fetch(message_id, "(RFC822)")
            if status == "OK":
                # Parse the email message
                message = email.message_from_bytes(message_data[0][1])
                subject, encoding = decode_header(message["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")

                # Print the subject of the new email
                print(f"New email: {subject}")

    # Sleep for a while before checking again (e.g., every 60 seconds)
    import time
    time.sleep(1)

# Close the IMAP connection (optional)
imap.logout()