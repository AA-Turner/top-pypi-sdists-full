import smtplib
import imaplib
import email
from email.mime.text import MIMEText
import uuid
import time
import os
from dotenv import load_dotenv

load_dotenv()

def send_and_wait():
    bridge_email = os.environ.get("SAGE_BRIDGE_EMAIL")
    password = os.environ.get("SAGE_BRIDGE_APP_PASSWORD")
    if not bridge_email or not password:
        print("Missing credentials")
        return
    
    unique_id = str(uuid.uuid4())
    print(f"Sending email with ID: {unique_id}")
    
    msg = MIMEText(f"Test prompt {unique_id}")
    msg["Subject"] = f"Test Task {unique_id}"
    msg["From"] = bridge_email
    msg["To"] = bridge_email
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(bridge_email, password)
    server.send_message(msg)
    server.quit()
    
    print("Email sent. Waiting for reply...")

send_and_wait()
