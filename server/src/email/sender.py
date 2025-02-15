import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid

class EmailSender:
    def __init__(self, smtp_config):
        self.config = smtp_config
        self.tracking_ids = {}

    def create_tracking_id(self, recipient):
        tracking_id = str(uuid.uuid4())
        self.tracking_ids[tracking_id] = recipient
        return tracking_id

    def send_phishing_email(self, recipient, subject, template, tracking_url):
        tracking_id = self.create_tracking_id(recipient)
        tracked_template = template.replace(
            "{TRACKING_LINK}", 
            f"{tracking_url}?id={tracking_id}"
        )

        msg = MIMEMultipart()
        msg['From'] = self.config['sender_email']
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(tracked_template, 'html'))

        with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
            server.starttls()
            server.login(self.config['sender_email'], self.config['password'])
            server.send_message(msg)

        return tracking_id