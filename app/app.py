from flask import Flask, render_template, session, redirect, request
import re
from utils import security
import secrets
from database import Database
from gmail import Email

# Database application setup
database = Database('localhost', 'root', '', 'social')

# Application Instance
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
database.init(app)

# Application routes
## Index route
@app.route('/')
def index():
    database.connect()
    database.open_cursor()

    database.cursor.execute("SELECT posts.id, posts.title, users.username, posts.created_at, posts.content FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC")
    posts = database.cursor.fetchall()

    database.close_cursor()
    return render_template('index.html', posts=posts)

## Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' in session:

        database.connect()
        database.open_cursor()

        database.cursor.execute("SELECT posts.id, posts.title, users.username, posts.created_at, posts.content FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC")
        posts = database.cursor.fetchall()

        database.close_cursor()
        return render_template('dashboard.html', posts=posts)
    return redirect('/login')

## Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/dashboard')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        database.connect()
        database.open_cursor()
        database.cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, username))
        user = database.cursor.fetchone()

        if user:
            hashed_password = user[2]
            if security.check_password(password, hashed_password):
                session['username'] = username
                database.close_cursor()
                return redirect('/dashboard')
        
        database.close_cursor()
        return render_template('login.html', error='Usuário/email ou senha estão incorretos.')
    return render_template('login.html')

## Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect('/dashboard')
    
    if request.method == 'POST':
        email_template = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        email = request.form['email']
        if re.match(email_template, email):
            username = request.form['username']
            password = request.form['password']

            database.connect()
            database.open_cursor()

            database.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            existing_user = database.cursor.fetchone()

            if existing_user:
                error = 'Este nome de usuário ou e-mail já estão registrados.'
                return render_template('register.html', error=error)

            hashed_password = security.hash_password(password)
            database.cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, hashed_password, email))
            database.connection.commit()
            database.close_cursor()

            session['username'] = username

            email_sender = Email()
            email_sender.send_email('Bem-vindo à Pawn Network', f"""
                <h1>Olá <strong>{username}</strong>,</h1>
                <p>Estamos muito felizes pelo seu interesse em fazer parte da nossa comunidade.</p>
                <p>Esperamos que você adquira e partilhe muito conhecimento e, a partir disso, ajude novos usuários.</p>
                <p>Caso deseje, clique no botão abaixo para conhecer a nossa dashboard.</p>
                <button><a href=http://127.0.0.1:5000/dashboard>Dashboard</button>
                <p>Atenciosamente,</p>
                <p><strong>Pawn Network.</strong></p>""", email)

            return redirect('/dashboard')
        else:
            error = 'O e-mail fornecido contém um padrão inválido.'
            return render_template('register.html', error=error)
    return render_template('register.html')

## Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

## New post route
@app.route('/new_post')
def new_post():
    return render_template('new_post.html')

## Change password route
@app.route('/change_password')
def change_password():
    return render_template('change_password.html')

## Verify password route
@app.route('/verify_email')
def verify_email():
    return render_template('verify_email.html')

## Create post route
@app.route('/create_post', methods=['POST'])
def create_post():
    if 'username' in session:
        username = session['username']
        content = request.form['content']
        title = request.form['title']

        database.connect()
        database.open_cursor()

        database.cursor.execute("SELECT id FROM users WHERE username = %s", (username))
        user_id = database.cursor.fetchone()[0]

        database.cursor.execute("INSERT INTO posts (user_id, title, content, created_at) VALUES (%s, %s, %s, NOW())", (user_id, title, content))
        database.connection.commit()
        database.close_cursor()

    return redirect('/dashboard')
