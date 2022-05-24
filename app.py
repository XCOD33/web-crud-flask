from flask import Flask, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pbop-pertemuan-11'
app.secret_key = 'ewd34r45y56u6yht'

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET' and 'loggedIn' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user")
        users = cur.fetchall()
        cur.close()

        return render_template('index.html', users=users)
    if request.method == 'GET':
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET','POST'])
def login():

    if request.method == 'GET' and 'loggedIn' in session:
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()

        if user:
            if bcrypt.hashpw(password, user[2].encode('utf-8')) == user[2].encode('utf-8'):
                session['loggedIn'] = True
                session['name'] = user[3]

                return redirect(url_for('index'))
            else:
                return "Email & Password doesn't match"

        return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET' and 'loggedIn' in session:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        fullname = request.form['fullname']
        phone = request.form['phone']

        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (username, password, fullname, phone) VALUES (%s, %s, %s, %s)", (username, hash_password, fullname, phone))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

@app.route('/logout', methods=['GET','POST'])
def logout():
    if request.method == 'GET':
        return redirect(url_for('index'))
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)