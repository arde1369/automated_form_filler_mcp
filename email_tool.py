"""
Email tool: sends email with optional attachment via Office 365 SMTP.

Credentials are read from environment variables:
    O365_EMAIL    - your Office 365 email address (sender)
    O365_PASSWORD - your Office 365 password or app password

For accounts with MFA enabled, generate an App Password in your Microsoft
account security settings and use that as O365_PASSWORD.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587


def send_email(
    recipients: list[str],
    subject: str,
    body: str,
    attachment_path: str = None,
    cc: list[str] = None,
    is_html: bool = False
) -> dict:
    """
    Send an email via Office 365 SMTP.

    Args:
        recipients:      List of TO email addresses.
        subject:         Email subject.
        body:            Email body (plain text or HTML).
        attachment_path: Optional path to a file to attach.
        cc:              Optional list of CC addresses.
        is_html:         True if body is HTML.

    Returns:
        Dict with status and delivery summary.
    """
    sender_email = os.environ.get("O365_EMAIL")
    sender_password = os.environ.get("O365_PASSWORD")

    if not sender_email or not sender_password:
        return {
            "error": (
                "Missing credentials. Set O365_EMAIL and O365_PASSWORD "
                "environment variables."
            )
        }

    if not recipients:
        return {"error": "No recipients provided."}

    cc = cc or []

    # Build the MIME message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    if cc:
        msg["Cc"] = ", ".join(cc)

    content_type = "html" if is_html else "plain"
    msg.attach(MIMEText(body, content_type))

    # Attach file if provided
    attached_filename = None
    if attachment_path:
        if not os.path.isfile(attachment_path):
            return {"error": f"Attachment not found: {attachment_path}"}
        attached_filename = os.path.basename(attachment_path)
        try:
            with open(attachment_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{attached_filename}"'
            )
            msg.attach(part)
        except Exception as e:
            return {"error": f"Failed to attach file: {e}"}

    # Send via Office 365 SMTP
    all_recipients = recipients + cc
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, all_recipients, msg.as_string())
    except smtplib.SMTPAuthenticationError:
        return {
            "error": (
                "SMTP authentication failed. Check O365_EMAIL and O365_PASSWORD. "
                "If MFA is enabled, use an App Password."
            )
        }
    except smtplib.SMTPException as e:
        return {"error": f"SMTP error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

    return {
        "status": "success",
        "sent_to": recipients,
        "cc": cc,
        "subject": subject,
        "attachment": attached_filename,
        "smtp_server": f"{SMTP_SERVER}:{SMTP_PORT}",
    }
