import smtplib
import ssl
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import re

# File paths
mail_content_file_path = r"Enter your mail_content.html file path..."
logo_path = r"Enter your logo_path..."

def check_email_address(s):
    # Email pattern regex
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return bool(re.match(pat, s))

def get_body():
    # Read email body from file
    with open(mail_content_file_path, encoding='utf-8') as f:
        body = f.read()
    return body

def send_email(recipient_email):
    # Login credentials
    sender_email = "enter your email address"
    password = "enter your email password"

    body = get_body()
    subject = "Enter email subject"

    # Email configuration
    message = MIMEMultipart("related")
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Add email content
    msg_alternative = MIMEMultipart("alternative")
    message.attach(msg_alternative)
    msg_alternative.attach(MIMEText(body, "html"))

    # Add image attachment
    with open(logo_path, 'rb') as img:
        msg_image = MIMEImage(img.read())
        msg_image.add_header('Content-ID', '<logo>')
        message.attach(msg_image)

    # Use a secure SSL context
    context = ssl.create_default_context()

    print("Sending email...")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email was sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: send_email.py [email_address]")
        sys.exit(1)
    recipient_email = sys.argv[1]
    if check_email_address(recipient_email):
        send_email(recipient_email)
    else:
        print("Invalid email address.")