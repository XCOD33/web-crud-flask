from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pbop-pertemuan-11'

mysql = MySQL(app)

@app.route('/form')
def form():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user")
    users = cur.fetchall()
    cur.close()

    return render_template('form.html', users=users)

@app.route('/submit', methods = ['GET','POST'])
def submit():
    if request.method == 'GET':
        return redirect(url_for('form'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (username, password, fullname, phone) VALUES (%s, %s, %s, %s)", (username, password, fullname, phone))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('submit'))

if __name__ == "__main__":
    app.run(debug=True)