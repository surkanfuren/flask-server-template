from flask import Flask, render_template, redirect, request, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

# conn = sqlite3.connect('database.db',check_same_thread=False)

try:
    conn = sqlite3.connect('database.db',check_same_thread=False)
    cursor = conn.cursor()
    print("Connection succesfull")
except sqlite3.Error as e:
    print(f"Connection error:{e}")
    cursor = conn.cursor()

# PAGE ROUTES

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/login')
def login():
    return render_template('pages/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = None
    if request.method == "POST":
        email = request.form['email']
        password_first = request.form['password']
        password = hash_password(password_first)
        if is_email_used(email):
            message = "This e-mail is already in use. Please choose another mail or log in to your account!"
        else:
            session["mail_in_use"] = False
            cursor.execute("INSERT INTO users(user_mail,user_pass) VALUES(?,?)", (email, password))
            conn.commit()
            return redirect("/login")

    return render_template('pages/signup.html', message=message)

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/pricing')
def pricing():
    return render_template('pages/pricing.html')

@app.route('/faq')
def faq():
    return render_template('pages/faq.html')

@app.route('/login-handler', methods=['POST'])
def login_handler():
    email = request.form["email"]
    password_first = request.form["password"]
    password = hash_password(password_first)
    cursor.execute("SELECT user_id FROM users where user_mail =? AND user_pass =?",(email,password))
    search = cursor.fetchone()


    return redirect("/")

# FUNCTIONAL GATEWAYS...
def is_email_used(email):
    cursor.execute("SELECT user_id FROM users WHERE user_mail=?",(email,))
    already_registered = cursor.fetchone()
    return already_registered is not None

def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_password = sha256.hexdigest()
    return hashed_password

if __name__ == '__main__':
    app.run(debug=True)