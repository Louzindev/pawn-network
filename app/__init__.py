from flask import Flask, render_template, request, redirect, session
from flaskext.mysql import MySQL
import re
import secrets
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
mysql = MySQL()


app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'social'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

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

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                error = 'Este nome de usuário ou e-mail já estão registrados.'
                return render_template('register.html', error=error)

            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            conn.commit()
            cursor.close()

            session['username'] = username
            return redirect('/dashboard')
        else:
            error = 'O e-mail fornecido contém um padrão inválido.'
            return render_template('register.html', error=error)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/dashboard')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s AND password = %s", (username, username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['username'] = username
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Usuário/email ou senha estão incorretos.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT posts.content, posts.created_at, users.username FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC")
        posts = cursor.fetchall()

        cursor.close()
        return render_template('dashboard.html', username=username, posts=posts)
    return redirect('/login')

@app.route('/create_post', methods=['POST'])
def create_post():
    if 'username' in session:
        username = session['username']
        content = request.form['content']

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s", (username))
        user_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO posts (user_id, content, created_at) VALUES (%s, %s, NOW())", (user_id, content))
        conn.commit()
        cursor.close()

    return redirect('/dashboard')

@app.route('/new_post')
def new_post():
    return render_template('new_post.html')

if __name__ == '__main__':
    app.run(debug=True)