import smtplib
import os
import random
import email.utils
from email.mime.text import MIMEText
from datetime import date

# ---------------- CONFIG ----------------
BIRTHDAY_MONTH = 9
BIRTHDAY_DAY = 23
TO_EMAIL = "aadi9varshney@gmail.com"
TO_NAME = "Bhoomika"

# Adding a sender name helps bypass spam filters by making the 'From' header look human
SENDER_NAME = "A Bhoomika Pagalu" 

GUESS_PAGE_URL = os.environ.get("GUESS_PAGE_URL", "https://YOUR_USERNAME.github.io/YOUR_REPO/")

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
# -----------------------------------------

MESSAGES = [
    "Quarterly review of your awesomeness is due in {days} day(s) — spoiler: you're crushing every KPI of being amazing.",
    "Reminder: your birthday deadline is approaching. No extensions. No exceptions. {days} day(s) left on the clock.",
    "Breaking news from the corporate world: {days} day(s) until the most important stakeholder meeting of the year — your birthday.",
    "Your out-of-office auto-reply for 'turning a year more wonderful' kicks in {days} day(s) from now.",
    "Someone's getting promoted to 'Officially One Year Cooler' — effective in {days} day(s).",
    "This is your {days}-day notice: the world is about to get a little brighter.",
    "Just a friendly ping (not a Slack notification) — {days} day(s) left till your big day.",
    "Filing this under 'important and worth celebrating': {days} day(s) to go.",
    "T-minus {days} day(s). Cake pending approval. Approval status: definitely approved.",
    "Adding this to your calendar: {days} day(s) until your birthday sprint begins.",
    "Performance review update: you've exceeded expectations all year. Celebration scheduled in {days} day(s).",
    "Following up on an open ticket: 'Missing: one birthday celebration.' ETA {days} day(s).",
]

def build_email(days):
    subject = f"{days} day{'s' if days != 1 else ''} to go, {TO_NAME}"
    random_message = random.choice(MESSAGES).format(days=days)
    
    # Constructing a clean, plain-text body
    text = f"Hey {TO_NAME} 👋\n\n"
    text += f"{random_message}\n\n"
    text += f"{days} day(s) left\n\n"
    text += "Curious who's sending these? You get 3 guesses a day. Hint: find my nickname.\n"
    text += f"Guess who I am here: {GUESS_PAGE_URL}\n\n"
    text += "Sent at midnight, just for you."
    
    return subject, text

def birthday_email():
    subject = f"Happy birthday, {TO_NAME}"
    
    text = f"Happy Birthday, {TO_NAME}! 🎂\n\n"
    text += "Hope today is as amazing as you are. Enjoy every bit of it!\n\n"
    text += "Still haven't guessed who's been sending these? You've got 3 tries a day. Hint: find my nickname.\n"
    text += f"Guess who I am here: {GUESS_PAGE_URL}\n"
    
    return subject, text

def send():
    today = date.today()
    bday_this_year = date(today.year, BIRTHDAY_MONTH, BIRTHDAY_DAY)

    if today > bday_this_year:
        print("This year's birthday has already passed. Skipping send.")
        return

    days = (bday_this_year - today).days

    if days == 0:
        subject, text = birthday_email()
    else:
        subject, text = build_email(days)

    # Use MIMEText directly for a plain text email
    msg = MIMEText(text, "plain", "utf-8")
    msg["Subject"] = subject
    
    # Format the From header to include a human-readable display name
    msg["From"] = f"{SENDER_NAME} <{GMAIL_USER}>"
    msg["To"] = TO_EMAIL
    
    # --- ANTI-SPAM HEADERS ---
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Message-ID"] = email.utils.make_msgid(domain="gmail.com")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())

    print(f"Sent plain text email successfully. Days remaining: {days}")

if __name__ == "__main__":
    send()
