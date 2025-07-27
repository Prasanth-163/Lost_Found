from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
#need to add otp
import random
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure random key

# MySQL connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Vasu@1122',  # Your MySQL root password
    database='flask_auth'
)
cursor = conn.cursor()

@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect('/login')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # ✅ Check for valid college email domain
    if not email.endswith('@anurag.edu.in'):
        flash('Invalid email format. Please use your college email (e.g., 22eg110b63@anurag.edu.in).', 'danger')
        return redirect('/login')

    # ✅ Check if email already registered
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        flash('This email already exists. Please enter a different email.', 'danger')
        return redirect('/login')

    # ✅ Register new user
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                   (username, email, hashed_password))
    conn.commit()
    flash('Registered Successfully. Please Login.', 'success')
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
            return redirect('/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

