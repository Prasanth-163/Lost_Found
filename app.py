from flask import Flask, render_template, request, redirect, session, flash, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import random, smtplib

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# MySQL connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Vasu@1122',  # your password
    database='flask_auth'
)
cursor = conn.cursor()

# Temporary store for OTPs
otp_storage = {}

# Email credentials
EMAIL_ADDRESS = '22eg110b63@anurag.edu.in'       # 🔁 Replace with your Gmail
EMAIL_PASSWORD = 'kult etzn mcmi mlzb'         # 🔁 Use App Password or enable less secure apps

@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html', username=session['username'])
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT id, username, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/')
        else:
            flash('Invalid Credentials.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if not email.endswith('@anurag.edu.in'):
        flash('Invalid email. Use your college email only.', 'danger')
        return redirect('/login')

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        flash('This email already exists. Please use a different email.', 'danger')
        return redirect('/login')

    if email not in otp_storage or otp_storage[email]['verified'] != True:
        flash('Please verify your email with OTP before registering.', 'danger')
        return redirect('/login')

    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                   (username, email, hashed_password))
    conn.commit()
    del otp_storage[email]
    flash('Registered successfully! Please login.', 'success')
    return redirect('/login')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data['email']

    if not email.endswith('@anurag.edu.in'):
        return jsonify({'message': 'Enter a valid college email (@anurag.edu.in)'}), 400

    otp = str(random.randint(100000, 999999))
    otp_storage[email] = {'otp': otp, 'verified': False}

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            subject = 'Your OTP for Email Verification'
            body = f'Your OTP is: {otp}'
            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(EMAIL_ADDRESS, email, msg)
        return jsonify({'message': 'OTP sent successfully'})
    except Exception as e:
        return jsonify({'message': 'Failed to send OTP', 'error': str(e)}), 500

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data['email']
    entered_otp = data['otp']

    if email in otp_storage and otp_storage[email]['otp'] == entered_otp:
        otp_storage[email]['verified'] = True
        return jsonify({'verified': True, 'message': 'Email verified successfully!'})
    return jsonify({'verified': False, 'message': 'Incorrect OTP. Try again.'})

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
