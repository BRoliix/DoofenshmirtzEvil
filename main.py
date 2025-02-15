import smtplib
from email.mime.text import MIMEText
spoof_sender = "noreply@amazon.com"  # The sender that will appear in the email
recipient = "johndoe@gmail.com"    # The recipient's email address

tracking_link = "http://localhost:5000/track?email=johndoe@example.com"

html_body = f"""
<html>
  <body>
    <p>Hello,</p>
    <p></p>
    <p><a href="{tracking_link}">Click here to confirm</a></p>
  </body>
</html>
"""

subject = "Test Spoof Email with Tracking Link"
msg = MIMEText(html_body, "html")
msg["Subject"] = subject
msg["From"] = spoof_sender  # Spoofed sender address
msg["To"] = recipient

with smtplib.SMTP("localhost", 1025) as smtp:
    smtp.sendmail(spoof_sender, recipient, msg.as_string())

print("Email with tracking link sent to MailHog.")
