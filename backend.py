from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from flask_cors import CORS
import os  # For environment variables

app = Flask(__name__)
CORS(app)

# Get email credentials from environment variables
EMAIL_ADDRESS = os.getenv("kariukisamuel866@gmail.com")
EMAIL_PASSWORD = os.getenv("hyan eala ntxa srye")
RECEIVER_EMAIL = EMAIL_ADDRESS  # Emails sent to yourself

@app.route("/")
def home():
    return "Backend is running! Use /contact to send messages."

@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    # Compose the email
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    msg = MIMEText(body)
    msg["Subject"] = "New Contact Form Submission"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
