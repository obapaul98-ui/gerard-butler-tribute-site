import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.resend.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@gerardbutlerofficial.com")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@gerardbutlerofficial.com")


def get_admin_html(fan_name: str, fan_email: str, message: str) -> str:
    """Admin notification — clean, light-themed to avoid spam filters on new domains."""
    return f"""
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; color: #222; max-width: 580px; margin: 0 auto; padding: 24px; background: #ffffff;">
  <p style="font-size: 14px; color: #666; margin: 0 0 16px 0;">New fan club message</p>
  <table style="width: 100%; margin: 0 0 16px 0; border-collapse: collapse;">
    <tr>
      <td style="color: #888; padding: 8px 0; width: 60px; font-size: 14px; vertical-align: top;">From</td>
      <td style="padding: 8px 0; font-size: 15px; font-weight: 600;">{fan_name}</td>
    </tr>
    <tr>
      <td style="color: #888; padding: 8px 0; font-size: 14px; vertical-align: top;">Email</td>
      <td style="padding: 8px 0; font-size: 15px;"><a href="mailto:{fan_email}" style="color: #1a73e8; text-decoration: none;">{fan_email}</a></td>
    </tr>
  </table>
  <div style="background: #f5f5f5; padding: 16px 20px; border-radius: 8px; border-left: 3px solid #1a73e8;">
    <p style="white-space: pre-wrap; font-size: 15px; line-height: 1.6; margin: 0; color: #333;">{message}</p>
  </div>
  <p style="font-size: 12px; color: #999; margin-top: 24px; padding-top: 16px; border-top: 1px solid #eee;">
    Automated notification from gerardbutlerofficial.com
  </p>
</body>
</html>
"""


def get_verification_admin_html(fan_name: str, fan_email: str, phone: str, address: str) -> str:
    """Notification sent to admin when a user submits their VIP profile with photo."""
    return f"""
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; color: #222; max-width: 580px; margin: 0 auto; padding: 24px; background: #ffffff;">
  <p style="font-size: 14px; color: #666; margin: 0 0 16px 0;">New VIP Profile Submission</p>
  <table style="width: 100%; margin: 0 0 16px 0; border-collapse: collapse;">
    <tr>
      <td style="color: #888; padding: 8px 0; width: 80px; font-size: 14px; vertical-align: top;">Name</td>
      <td style="padding: 8px 0; font-size: 15px; font-weight: 600;">{fan_name}</td>
    </tr>
    <tr>
      <td style="color: #888; padding: 8px 0; font-size: 14px; vertical-align: top;">Email</td>
      <td style="padding: 8px 0; font-size: 15px;"><a href="mailto:{fan_email}">{fan_email}</a></td>
    </tr>
    <tr>
      <td style="color: #888; padding: 8px 0; font-size: 14px; vertical-align: top;">Phone</td>
      <td style="padding: 8px 0; font-size: 15px;">{phone}</td>
    </tr>
    <tr>
      <td style="color: #888; padding: 8px 0; font-size: 14px; vertical-align: top;">Address</td>
      <td style="padding: 8px 0; font-size: 15px;">{address}</td>
    </tr>
  </table>
  <div style="background: #e8f0fe; padding: 16px; border-radius: 8px; color: #1a73e8; font-size: 14px;">
    <strong>Photo Attached:</strong> Please check the attachments for the fan's uploaded photo.
  </div>
</body>
</html>
"""

def get_fan_html(fan_name: str, fan_email: str = "") -> str:
    """Fan auto-reply — using the user's provided Code 2 (Dark Blue Canvas with Form)."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerard Butler Fan Club • Membership</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Georgia&display=swap');
        
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            color: #e0f0ff;
            background: #0a1a2f;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 620px;
            margin: 20px auto;
            background: linear-gradient(180deg, #0f253f 0%, #0a1a2f 100%);
            border: 8px solid #1e4a7a;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0, 30, 80, 0.6);
        }}
        .header {{
            background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.6)), url('https://picsum.photos/id/1015/1200/400') center/cover;
            padding: 60px 30px 40px;
            text-align: center;
            position: relative;
        }}
        .header::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: linear-gradient(to right, #1e90ff, #00b4d8);
        }}
        .logo {{
            font-family: 'Playfair Display', serif;
            font-size: 42px;
            color: #ffffff;
            text-shadow: 0 4px 15px rgba(30, 144, 255, 0.7);
            letter-spacing: 2px;
            margin: 0;
        }}
        .subtitle {{
            color: #a0d8ff;
            font-size: 18px;
            margin-top: 8px;
            letter-spacing: 3px;
        }}
        .content {{
            padding: 40px 35px;
            line-height: 1.7;
        }}
        h2 {{
            color: #4fc3f7;
            text-align: center;
            font-size: 26px;
            margin-bottom: 30px;
            border-bottom: 2px solid #1e90ff;
            padding-bottom: 12px;
        }}
        .form-group {{
            margin-bottom: 22px;
        }}
        label {{
            display: block;
            margin-bottom: 8px;
            color: #b0d4ff;
            font-weight: bold;
        }}
        input[type="text"], input[type="tel"], textarea {{
            width: 100%;
            padding: 14px 18px;
            background: #112a4a;
            border: 2px solid #1e4a7a;
            border-radius: 6px;
            color: #e0f0ff;
            font-size: 16px;
            box-sizing: border-box;
        }}
        input[type="file"] {{
            width: 100%;
            padding: 10px;
            background: #112a4a;
            border: 2px dashed #1e90ff;
            border-radius: 6px;
            color: #e0f0ff;
        }}
        .btn {{
            display: block;
            width: 100%;
            background: linear-gradient(to right, #1e90ff, #00b4d8);
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 16px;
            border: none;
            border-radius: 6px;
            margin-top: 30px;
            cursor: pointer;
            box-shadow: 0 6px 20px rgba(30, 144, 255, 0.4);
        }}
        .btn:hover {{
            background: linear-gradient(to right, #00b4d8, #1e90ff);
        }}
        .canvas-bg {{
            background-image: 
                linear-gradient(rgba(30, 144, 255, 0.08) 1px, transparent 1px),
                linear-gradient(90deg, rgba(30, 144, 255, 0.08) 1px, transparent 1px);
            background-size: 40px 40px;
        }}
        .footer {{
            background: #081526;
            padding: 30px;
            text-align: center;
            font-size: 14px;
            color: #7799cc;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1 class="logo">GERARD BUTLER</h1>
            <p class="subtitle">OFFICIAL FAN CLUB</p>
        </div>

        <!-- Body -->
        <div class="content canvas-bg">
            <p style="font-size: 17px; text-align: center; margin-bottom: 32px;">
                Welcome to the family, {fan_name}! Become a verified member and connect with fellow fans.
            </p>

            <h2>Complete Your VIP Registration</h2>

            <div style="background: rgba(30, 144, 255, 0.08); border: 1px solid #1e4a7a; border-radius: 8px; padding: 25px; margin-bottom: 30px; text-align: left;">
                <p style="margin-top: 0; margin-bottom: 20px; font-size: 16px; color: #a0d8ff;">To verify your identity and finalize your exclusive membership, please securely provide the following details:</p>
                <ul style="list-style-type: none; padding: 0; margin: 0; font-size: 16px; color: #e0f0ff; line-height: 1.8;">
                    <li style="margin-bottom: 8px;"><strong style="color: #4fc3f7;">✓</strong> Full Legal Name</li>
                    <li style="margin-bottom: 8px;"><strong style="color: #4fc3f7;">✓</strong> Phone Number</li>
                    <li style="margin-bottom: 8px;"><strong style="color: #4fc3f7;">✓</strong> Home Address <span style="font-size: 13px; color: #88aacc;">(for exclusive merchandise)</span></li>
                    <li style="margin-bottom: 0;"><strong style="color: #4fc3f7;">✓</strong> A recent profile photo <span style="font-size: 13px; color: #88aacc;">(attached)</span></li>
                </ul>
            </div>

            <a href="https://gerardbutlerofficial.com/verify?email={fan_email}" style="display: block; width: 100%; box-sizing: border-box; text-align: center; background: linear-gradient(to right, #1e90ff, #00b4d8); color: white; font-size: 18px; font-weight: bold; padding: 18px; border-radius: 6px; text-decoration: none; margin-top: 10px; box-shadow: 0 6px 20px rgba(30, 144, 255, 0.4);">CLICK HERE TO COMPLETE VIP PROFILE</a>

            <p style="text-align: center; margin-top: 35px; font-size: 15px; color: #88aacc;">
                Your information is safe with us. We respect your privacy.
            </p>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p><strong>The Gerard Butler Fan Club Team</strong></p>
            <p>gerardbutlerofficial.com • Official Fan Community</p>
            <p style="margin-top: 15px; font-size: 12px;">
                © 2026 Gerard Butler Fan Club • All Rights Reserved
            </p>
        </div>
    </div>
</body>
</html>
"""


def send_email(to_email: str, subject: str, text_content: str, html_content: str, attachment=None):
    if not SMTP_USER or not SMTP_PASS:
        print(f"Skipping email to {to_email} because SMTP credentials are not set in .env")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = f"Gerard Butler Fan Club <{FROM_EMAIL}>"
    msg['To'] = to_email

    # Plain text first (improves spam score — high text-to-HTML ratio)
    msg.set_content(text_content)
    msg.add_alternative(html_content, subtype='html')

    if attachment:
        filename, content_type, file_data = attachment
        maintype, subtype = content_type.split('/', 1) if '/' in content_type else ('application', 'octet-stream')
        msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)

    try:
        # Resend uses SSL on port 465 (not STARTTLS on 587)
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()

        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent successfully to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
