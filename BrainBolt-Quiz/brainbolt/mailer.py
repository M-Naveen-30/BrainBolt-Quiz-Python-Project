"""
mailer.py
~~~~~~~~~
Sends the generated certificate (PDF attachment) via Gmail SMTP.
Uses smtplib + ssl + email.mime - standard library only.
"""
import os
import smtplib
import ssl
from email.message import EmailMessage

from .config import load_email_config


class Mailer:
    """Sends an HTML email with a PDF certificate attachment."""

    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 465   # SSL

    def __init__(self):
        cfg = load_email_config()
        self._sender   = cfg["sender_email"]
        self._app_pass = cfg["sender_app_pass"]
        self._name     = cfg["sender_name"] or "BrainBolt"

    # ----------------------------------------------------------------
    def is_configured(self) -> bool:
        return (self._sender and self._app_pass and
                "@" in self._sender and
                self._sender != "your_email@gmail.com" and
                self._app_pass != "your16charapppass")

    # ----------------------------------------------------------------
    def send_certificate(self, to_email: str, user_name: str,
                         topic_label: str, score: int, total: int,
                         tier: str, pdf_path: str) -> bool:
        if not self.is_configured():
            print("   (Gmail not configured in config.ini - skipping email)")
            print(f"   Your certificate is saved locally at:\n      {pdf_path}")
            return False

        msg              = EmailMessage()
        msg["Subject"]   = f"BrainBolt - Your {tier} Certificate ({topic_label})"
        msg["From"]      = f"{self._name} <{self._sender}>"
        msg["To"]        = to_email

        body = (
            f"Hi {user_name},\n\n"
            f"Congratulations on completing the BrainBolt quiz on {topic_label}!\n"
            f"You scored {score} / {total} and earned a {tier} certificate.\n\n"
            f"Your certificate is attached to this email.\n\n"
            f"Keep learning, keep sparking!\n"
            f"-- The BrainBolt Team --"
        )
        msg.set_content(body)

        # attach the PDF
        try:
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            msg.add_attachment(
                pdf_data,
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(pdf_path),
            )
        except FileNotFoundError:
            print(f"   PDF not found: {pdf_path}")
            return False

        # SSL send
        try:
            ctx = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.SMTP_HOST, self.SMTP_PORT, context=ctx) as srv:
                srv.login(self._sender, self._app_pass)
                srv.send_message(msg)
            print(f"   Certificate emailed to {to_email}")
            return True
        except smtplib.SMTPAuthenticationError:
            print("   Gmail authentication failed.")
            print("   Tip: use a 16-char Gmail App Password, not your normal password.")
            print("        See https://myaccount.google.com/apppasswords")
            return False
        except Exception as e:
            print(f"   Could not send email: {e}")
            print(f"   Your certificate is saved locally at:\n      {pdf_path}")
            return False
