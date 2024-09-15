import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'YOUR EMAIL'
SMTP_PASSWORD = 'YOUR PASSWORD'


def send_email(name, email, subject, message):
    """Send an email using SMTP."""
    # Compose the email
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_USER  # Your email (you will receive the messages)
    msg['Subject'] = f"Contact Form Submission: {subject}"

    # The message content
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    # Set up the SMTP server and send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Enable TLS
        server.login(SMTP_USER, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USER, SMTP_USER, text)  # From and To are your email
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
