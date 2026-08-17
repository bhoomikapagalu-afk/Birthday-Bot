import smtplib
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

# ---------------- CONFIG ----------------
BIRTHDAY_MONTH = 9
BIRTHDAY_DAY = 23
TO_EMAIL = "bugfinder1149@gmail.com"
TO_NAME = "Bhoomika"

# Set this to your GitHub Pages URL once it's live, e.g.
# https://yourusername.github.io/your-repo-name/
GUESS_PAGE_URL = os.environ.get("GUESS_PAGE_URL", "https://YOUR_USERNAME.github.io/YOUR_REPO/")

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
# -----------------------------------------

MESSAGES = [
    "Quarterly review of your awesomeness is due in {days} day(s) \u2014 spoiler: you're crushing every KPI of being amazing.",
    "Reminder: your birthday deadline is approaching. No extensions. No exceptions. {days} day(s) left on the clock.",
    "Breaking news from the corporate world: {days} day(s) until the most important stakeholder meeting of the year \u2014 your birthday.",
    "Your out-of-office auto-reply for 'turning a year more wonderful' kicks in {days} day(s) from now.",
    "Someone's getting promoted to 'Officially One Year Cooler' \u2014 effective in {days} day(s).",
    "This is your {days}-day notice: the world is about to get a little brighter.",
    "Just a friendly ping (not a Slack notification) \u2014 {days} day(s) left till your big day.",
    "Filing this under 'important and worth celebrating': {days} day(s) to go.",
    "T-minus {days} day(s). Cake pending approval. Approval status: definitely approved.",
    "Adding this to your calendar: {days} day(s) until your birthday sprint begins.",
    "Performance review update: you've exceeded expectations all year. Celebration scheduled in {days} day(s).",
    "Following up on an open ticket: 'Missing: one birthday celebration.' ETA {days} day(s).",
]


def build_email(days):
    subject = f"{days} day{'s' if days != 1 else ''} to go, {TO_NAME}"
    body_text = random.choice(MESSAGES).format(days=days)
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background:#fdf6f0; padding:24px;">
      <div style="max-width:480px;margin:auto;background:white;border-radius:16px;padding:24px;box-shadow:0 2px 10px rgba(0,0,0,0.08);">
        <h2 style="color:#d63384;">Hey {TO_NAME} 👋</h2>
        <p style="font-size:16px;color:#333;">{body_text}</p>
        <p style="font-size:28px;font-weight:bold;color:#6f42c1;text-align:center;margin:24px 0;">
          {days} day(s) left
        </p>
        <p style="font-size:15px;color:#555;">
          Curious who's sending these? You get <b>3 guesses a day</b>. Hint: <i>find my nickname</i>.
        </p>
        <p style="text-align:center;margin-top:20px;">
          <a href="{GUESS_PAGE_URL}" style="background:#d63384;color:white;padding:12px 20px;border-radius:8px;text-decoration:none;font-weight:bold;">
            Guess who I am →
          </a>
        </p>
        <p style="font-size:12px;color:#999;text-align:center;margin-top:30px;">Sent at midnight, just for you.</p>
      </div>
    </body>
    </html>
    """
    return subject, body_text, html


def birthday_email():
    subject = f"Happy birthday, {TO_NAME}"
    text = f"Happy Birthday {TO_NAME}! Hope today is as amazing as you are."
    html = f"""
    <html><body style="font-family:Arial,sans-serif;padding:24px;background:#fdf6f0;">
      <div style="max-width:480px;margin:auto;background:white;border-radius:16px;padding:24px;text-align:center;">
        <h1 style="color:#d63384;">Happy Birthday, {TO_NAME}! 🎂</h1>
        <p style="font-size:16px;color:#333;">Hope today is as amazing as you are. Enjoy every bit of it!</p>
        <p style="font-size:15px;color:#555;margin-top:20px;">
          Still haven't guessed who's been sending these? You've got 3 tries a day. Hint: <i>find my nickname</i>.
        </p>
        <p style="text-align:center;margin-top:20px;">
          <a href="{GUESS_PAGE_URL}" style="background:#d63384;color:white;padding:12px 20px;border-radius:8px;text-decoration:none;font-weight:bold;">
            Guess who I am →
          </a>
        </p>
      </div>
    </body></html>
    """
    return subject, text, html


def send():
    today = date.today()
    bday_this_year = date(today.year, BIRTHDAY_MONTH, BIRTHDAY_DAY)

    if today > bday_this_year:
        print("This year's birthday has already passed. Skipping send.")
        return

    days = (bday_this_year - today).days

    if days == 0:
        subject, text, html = birthday_email()
    else:
        subject, text, html = build_email(days)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())

    print(f"Sent email successfully. Days remaining: {days}")


if __name__ == "__main__":
    send()
