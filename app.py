from flask import Flask, render_template, request, redirect, session, flash, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import random, smtplib

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# -------------------- DATABASE --------------------
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Vasu@1122',
    database='flask_auth'
)
cursor = conn.cursor()

# -------------------- OTP STORAGE --------------------
otp_storage = {}

# -------------------- EMAIL CONFIG --------------------
EMAIL_ADDRESS = '22eg110b63@anurag.edu.in'
EMAIL_PASSWORD = 'ekxx glyo wezt bmjw'

# -------------------- ADMIN CREDENTIALS --------------------
ADMIN_EMAILS = [
    '22eg110b63@anurag.edu.in',
    '22eg110b06@anurag.edu.in'
]
ADMIN_PASSWORD = 'admin'

# -------------------- HOME --------------------
@app.route('/')
def home():
    if session.get('is_admin'):
        return render_template('home.html', username="Admin")

    if 'user_id' in session:
        return render_template('home.html', username=session['username'])

    return redirect('/login')

# -------------------- USER LOGIN --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT id, username, password FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session.clear()
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = False
            flash("Login successful", "success")
            return redirect('/')
        else:
            flash("Invalid Credentials", "danger")

    return render_template('login.html')

# -------------------- ADMIN LOGIN (IMPORTANT FIX) --------------------
@app.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form['email']
    password = request.form['password']

    if email in ADMIN_EMAILS and password == ADMIN_PASSWORD:
        session.clear()
        session['is_admin'] = True
        session['username'] = "Admin"
        flash("Admin login successful", "success")
        return redirect('/')

    flash("Invalid Admin Credentials", "danger")
    return redirect('/login')

# -------------------- REGISTER --------------------
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if not email.endswith('@anurag.edu.in'):
        flash("Use college email only", "danger")
        return redirect('/login')

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        flash("Email already exists", "danger")
        return redirect('/login')

    if email not in otp_storage or not otp_storage[email]['verified']:
        flash("Verify email with OTP first", "danger")
        return redirect('/login')

    hashed = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users(username,email,password) VALUES(%s,%s,%s)",
        (username, email, hashed)
    )
    conn.commit()
    del otp_storage[email]

    flash("Registered successfully", "success")
    return redirect('/login')

# -------------------- SEND OTP --------------------
@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data['email']

    otp = str(random.randint(100000, 999999))
    otp_storage[email] = {'otp': otp, 'verified': False}

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_ADDRESS, email, f"Subject: OTP\n\nYour OTP is {otp}")

    return jsonify({"message": "OTP sent"})

# -------------------- VERIFY OTP --------------------
@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data['email']
    otp = data['otp']

    if email in otp_storage and otp_storage[email]['otp'] == otp:
        otp_storage[email]['verified'] = True
        return jsonify({"verified": True, "message": "OTP verified"})

    return jsonify({"verified": False, "message": "Invalid OTP"})

# -------------------- LOGOUT --------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out", "success")
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
