from flask import Flask, render_template, request, session
import smtplib
from email.mime.text import MIMEText
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random string for session security

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    email = request.form['email']

    # Generate a random 6-digit OTP
    otp = str(random.randint(100000, 999999))

    # Store OTP in session
    session['otp'] = otp

    # Email configuration
    sender_email = 'youremail@gmail.com'  # Replace with your email address
    subject = 'Your OTP Code'
    body = f'Your OTP code is: {otp}'

    # Email server configuration (for Gmail)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'youremail@gmail.com'  # Replace with your email address
    smtp_password = 'yourpassword'  # Replace with your email password

    # Create a secure connection with the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Log in to your email account
    server.login(smtp_username, smtp_password)

    # Create the email message
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = email

    # Send the email
    server.sendmail(sender_email, [email], message.as_string())

    # Quit the server
    server.quit()

    return render_template('verify_otp.html')

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    user_otp = request.form['otp']

    if 'otp' in session and user_otp == session['otp']:
        return "Login successful!"
    else:
        return "Invalid OTP. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
