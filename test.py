from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# Replace with your actual Gmail and App Password
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '22eg110b63@anurag.edu.in'
app.config['MAIL_PASSWORD'] = 'kult etzn mcmi mlzb'

mail = Mail(app)

@app.route('/')
def send_test_mail():
    try:
        msg = Message('Test Email from Flask', sender=app.config['MAIL_USERNAME'], recipients=['your_email@gmail.com'])
        msg.body = 'If you received this email, Flask-Mail works fine!'
        mail.send(msg)
        return "✅ Mail sent successfully!"
    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
