from flask import Flask, render_template, request, flash, redirect
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")
# EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
# app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT'))
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_RECEIVER'] = os.environ.get('MAIL_RECEIVER')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') == 'True'
# app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL') == 'True'

MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT'))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_RECEIVER = os.environ.get('MAIL_RECEIVER')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') == 'True'
MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') == 'True'


@app.route("/")
def home():
    services = ["Phone Repair", "Laptop Repair", "TV Repair", "Washing Machine Fix", "Speaker Tuning"]
    return render_template("home.html", services=services)

@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        service = request.form["service"]
        date = request.form["date"]
        message = request.form["message"]

        email_body = f"""New Service Booking Request:
Name: {name}
Email: {email}
Service: {service}
Preferred Date: {date}
Message: {message}
"""
        try:
            send_email("New Booking Request", email_body)
            flash("Booking request sent successfully!", "success")
            return redirect("/book")
        except Exception as e:
            flash(f"Error sending email: {str(e)}", "danger")

    return render_template("book.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        email_body = f"""New Contact Message:
Name: {name}
Email: {email}
Message: {message}
"""
        try:
            send_email("New Contact Message", email_body)
            flash("Message sent successfully!", "success")
            return redirect("/contact")
        except Exception as e:
            flash(f"Error sending message: {str(e)}", "danger")

    return render_template("contact.html")

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = MAIL_USERNAME
    msg["To"] = MAIL_RECEIVER

    with smtplib.SMTP_SSL("mail.tillhappens.name.ng", 465) as server:
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    app.run(debug=True)