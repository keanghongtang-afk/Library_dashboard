import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Load from environment variables (set in .env)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("EMAIL_ADDRESS", "")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD", "")


def send_new_device_alert(recipient_email: str, user_name: str, device_id: str):
    """
    Send an email alert when a login is detected from a new/different device.

    Args:
        recipient_email: The user's email address.
        user_name: The user's display name.
        device_id: The identifier of the new device.
    """
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("[EmailService] SMTP credentials not configured. Skipping email.")
        return

    subject = "New Device Login Detected"
    login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: white; border-radius: 8px;
                    padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
          <h2 style="color: #d9534f;">⚠️ New Device Login Alert</h2>
          <p>Hello <strong>{user_name}</strong>,</p>
          <p>We detected a login to your account from a <strong>new or unrecognized device</strong>.</p>
          <table style="width:100%; border-collapse: collapse; margin: 16px 0;">
            <tr>
              <td style="padding: 8px; border: 1px solid #ddd; background:#f9f9f9;"><strong>Device ID</strong></td>
              <td style="padding: 8px; border: 1px solid #ddd;">{device_id}</td>
            </tr>
            <tr>
              <td style="padding: 8px; border: 1px solid #ddd; background:#f9f9f9;"><strong>Time</strong></td>
              <td style="padding: 8px; border: 1px solid #ddd;">{login_time}</td>
            </tr>
          </table>
          <p>If this was you, no action is needed. If you did <strong>not</strong> authorize this login,
             please change your password immediately.</p>
          <p style="color: #888; font-size: 12px;">This is an automated message from the Library Management System.<br>Do not reply to this email. Thank You!</p>
        </div>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        print(f"[EmailService] Alert sent to {recipient_email}")
    except Exception as e:
        print(f"[EmailService] Failed to send email: {e}")


def send_otp_email(recipient_email: str, user_name: str, otp: str):
    """
    Send an OTP verification email when the user logs in from a new/different device.

    Args:
        recipient_email: The user's email address.
        user_name: The user's display name.
        otp: The 6-digit OTP code.
    """
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("[EmailService] SMTP credentials not configured. Skipping OTP email.")
        return

    subject = "Your Device Verification Code"
    sent_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: white; border-radius: 8px;
                    padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
          <h2 style="color: #3a6fd8;">🔐 Device Verification</h2>
          <p>Hello <strong>{user_name}</strong>,</p>
          <p>We detected a login attempt from a <strong>new or unrecognized device</strong>.<br>
             Use the code below to verify and allow this device:</p>
          <div style="text-align: center; margin: 24px 0;">
            <span style="font-size: 36px; font-weight: bold; letter-spacing: 8px;
                         color: #3a6fd8; background: #eef2ff; padding: 12px 24px;
                         border-radius: 8px; display: inline-block;">
              {otp}
            </span>
          </div>
          <p style="color: #e05c5c;"><strong>⏱ This code expires in 5 minutes.</strong></p>
          <table style="width:100%; border-collapse: collapse; margin: 16px 0;">
            <tr>
              <td style="padding: 8px; border: 1px solid #ddd; background:#f9f9f9;"><strong>Sent At</strong></td>
              <td style="padding: 8px; border: 1px solid #ddd;">{sent_time}</td>
            </tr>
          </table>
          <p>If you did <strong>not</strong> attempt to log in, please change your password immediately.</p>
          <p style="color: #888; font-size: 12px;">This is an automated message from the Library Management System.<br>Do not reply to this email. Thank You!</p>
        </div>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        print(f"[EmailService] OTP sent to {recipient_email}")
    except Exception as e:
        print(f"[EmailService] Failed to send OTP email: {e}")
