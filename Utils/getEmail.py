import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
load_dotenv(env_path)

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

EMAIL_ADDRESS = os.getenv("GMAIL_ADDR")
EMAIL_PASSWORD = os.getenv("GMAIL_PASS")


def email_parser(stop_check):
    # Connect & login
    imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    imap.select("INBOX")

    print("Watching inbox... Press 'q' to stop.\n")

    while not stop_check():
        status, message_ids = imap.search(None, "UNSEEN")

        if status == "OK":
            message_ids = message_ids[0].split()

            for message_id in message_ids:
                status, message_data = imap.fetch(message_id, "(RFC822)")
                if status == "OK":
                    message = email.message_from_bytes(message_data[0][1])

                    subject, encoding = decode_header(message["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")

                    print(f"📩 New email: {subject}")

        time.sleep(1)

    print("\nStopping IMAP watcher...")
    imap.logout()
