from flask import Flask, render_template, request, abort, url_for, redirect, jsonify, send_from_directory
app = Flask(__name__)

import os, smtplib, ssl
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_USER = os.environ["GMAIL_USER"]          # your dedicated gmail address
GMAIL_APP_PASSWORD = os.environ["GMAIL_PASSWORD"]  # app password

def send_contact_email(name: str, email: str, message: str):
    msg = EmailMessage()
    msg["Subject"] = f"Portfolio Contact from {name}"
    msg["From"] = GMAIL_USER
    msg["To"] = os.environ.get("CONTACT_DEST", GMAIL_USER)  # where you receive it
    msg.set_content(f"From: {name} <{email}>\n\n{message}")

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls(context=context)
        smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)


@app.route("/")
def home():
    print("wtf")
    return render_template("index.html")  # create templates/index.html


@app.route("/api/contact/", methods=["POST"])
def contact():
    data = request.get_json()
    if not data:
        abort(400, "Missing fields")
    name = data.get("name")
    email = data.get("email")
    subject = data.get("subject")
    message = data.get("message")

    print(name, email, message)
    if not (name and email and message):
        abort(400, "Missing fields")

    # TODO: add basic validation, captcha, and rate-limit checks
    send_contact_email(name, email, message)
    return redirect(url_for("home"))

@app.get("/resume")
def resume():
    return send_from_directory(app.static_folder, "Ephraim_Bennett_Resume.pdf")


if __name__ == "__main__":
    # For local dev only; Cloud Run uses Gunicorn CMD above
    app.run(host="0.0.0.0", port=8080, debug=True)
