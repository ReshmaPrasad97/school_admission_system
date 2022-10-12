from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

#create flask instance
app = Flask(__name__)

#secret key
app.config['SECRET_KEY'] = "my super secret key"

#connect to mysql db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'admission'
 
mysql = MySQL(app)


#create route decorator
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = % s AND password = % s', (username, password ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            username=request.form.get('username')
            return redirect(url_for('admission'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))





@app.route('/admission', methods = ['GET', 'POST'])
def admission():
    msg = ''
    if request.method == 'POST' and 'stud_id' in request.form and 'username' in request.form  and 'dob' in request.form and 'academic_year' in request.form and 'fathers_name' in request.form and 'mothers_name' in request.form  and 'address' in request.form and 'contact' in request.form and 'email' in request.form and 'password' in request.form and 'class_id' in request.form:
        stud_id = request.form['stud_id']
        username = request.form['username']
        dob = request.form['dob']
        academic_year = request.form['academic_year']
        fathers_name=request.form['fathers_name']
        mothers_name=request.form['mothers_name']
        address=request.form['address']
        contact = request.form['contact']
        email = request.form['email']
        password = request.form['password']
        class_id =request.form['class_id']
       
        
       
       
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email or not dob or not address or not contact or not fathers_name or not mothers_name or not class_id  or not academic_year or not stud_id:
            msg = 'Please fill out the form !'
        else:
            # cursor.execute('INSERT INTO login(username,password) VALUES ( % s, % s)', (username, password, ))
            cursor.execute('INSERT INTO student(stud_id,username,dob,academic_year,fathers_name,mothers_name,address,contact,email,password,class_id) VALUES ( % s, % s, % s, % s, % s,% s,% s,% s,% s,% s, % s )', (stud_id,username,dob,academic_year,fathers_name,mothers_name,address,contact,email,password,class_id))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'                  
    return render_template('admission.html',msg = msg)




@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form  and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'phone' in request.form :
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
       
       
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email or not first_name or not last_name or not phone :
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO login(username,password) VALUES ( % s, % s)', (username, password, ))
            cursor.execute('INSERT INTO register(first_name,last_name,username,password,email,phone) VALUES ( % s, % s, % s, % s, % s,% s)', (first_name, last_name,username, password,email,phone))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


if __name__ == "__main__":
    app.run(debug=True)