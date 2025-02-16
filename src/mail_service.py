import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from datetime import datetime
import os

class MailService:
    def __init__(self, host="localhost", port=1025):
        self.host = host
        self.port = port
        self.tracking_file = "phishing_tracking.json"
    
    def send_email(self, email_content, target_email, metadata):
        """Send email to MailHog and track the attempt"""
        # Parse email content
        subject = email_content.split("SUBJECT:")[1].split("\n")[0].strip()
        body = email_content.split("EMAIL:")[1].split("SIGNATURE:")[0].strip()
        signature = email_content.split("SIGNATURE:")[1].strip()
        
        # Create message
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = "security.test@company.local"
        msg['To'] = target_email
        
        # Combine body and signature
        full_body = f"{body}\n\n{signature}"
        msg.attach(MIMEText(full_body, 'plain'))
        
        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.send_message(msg)
            self._track_email(target_email, metadata)
            return True
        except Exception as e:
            raise Exception(f"Failed to send email: {e}")
    
    def _track_email(self, target_email, metadata):
        """Track email sending attempt"""
        tracking_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'target_email': target_email,
            'organization': metadata['target_org'],
            'department': metadata['target_dept'],
            'scenario': metadata['scenario_type'],
            'status': 'sent'
        }
        
        try:
            tracking_list = []
            if os.path.exists(self.tracking_file):
                with open(self.tracking_file, 'r') as f:
                    tracking_list = json.load(f)
            
            tracking_list.append(tracking_data)
            
            with open(self.tracking_file, 'w') as f:
                json.dump(tracking_list, f, indent=4)
        except Exception as e:
            raise Exception(f"Error tracking email: {e}")
    
    def get_tracking_data(self):
        """Retrieve tracking data"""
        if os.path.exists(self.tracking_file):
            with open(self.tracking_file, 'r') as f:
                return json.load(f)
        return []
