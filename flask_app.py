from flask import Flask, render_template, redirect, request, url_for, session
import MySQLdb
from database import create_tables, add_test_data, read_user_data, read_planet_data, add_user, add_planet_data
from database import read_invitation_codes, check_credentials
from helper import hash_password, verify_password

app = Flask(__name__)
app.secret_key = 'super secret key2'

mysql = MySQLdb.connect(host="Exodus2200.mysql.pythonanywhere-services.com", user="Exodus2200", passwd="Excalibur_01", db="Exodus2200$exodus2200")



@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        cur = mysql.cursor()
        
    except:
        cur.close()
        cur = mysql.cursor()
        print()
    if session.get('logged_in'):
        message = ""
        if request.method == "POST":

            if request.form.get("L") == "logout":
                session.clear()
                return redirect(url_for('login_page'))


            return render_template('index.html',  message=message)
        else:
            message = "All systems operational"
            return render_template('index.html',  message=message)
    else:
        return redirect(url_for('login_page'))

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    message = ""
    if request.method == 'POST':
        cur = mysql.cursor()
        if request.form.get("R") == "register":
            return redirect(url_for('register'))
        else:
            message = "R is : " + str(request.form.get("R"))

        username = request.form['username']
        password = request.form['password']
        if username == "alex" and password == "csgo":
            session['logged_in'] = True
            session['admin'] = True
            cur.close()
            return redirect(url_for('home'))
        elif check_credentials(username, password, cur):
            message = "You are logged in as " + str(username)
            cur.close()
            session['logged_in'] = True
            session['admin'] = False
            return render_template("message.html", message=message, goto="/")
        else:
            cur.close()
            message="username unknown or wrong password"


    return render_template("login.html", message=message)


@app.route("/register", methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST':
        
        cur = mysql.cursor()
        valid_inv_codes = []
        stored_usernames = []
        data1 = read_invitation_codes(cur)
        data2 = read_user_data(cur)
        
        for d in data1:
            valid_inv_codes.append(d[1])

        for d in data2:
            stored_usernames.append(d[2])

        name = request.form['name']
        username = request.form['username']
        pssw1 = request.form['password1']
        pssw2 = request.form['password2']
        inv_code = request.form['invitation_code']
        level = 0

        if pssw1 != pssw2:
            message = "passwords don't match"
        elif inv_code not in valid_inv_codes:
            message = "wrong invitation code"
        elif username in stored_usernames:
            message = "username already exists"
        else:
            message = "You have been registered with username: " + str(username)
            password = hash_password(pssw1)
            add_user(cur, name, username, password, inv_code, level)
            cur.close()
            return render_template("message.html", message=message, goto="/login")
        cur.close()
        return render_template('register.html', message=message)
    return render_template('register.html', message=message)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    print("1")
    if session.get('admin'):
        print("2")
        cur = mysql.cursor()
        print("3")
        #create_tables(cur)
        #add_test_data(cur)
        users = read_user_data(cur)
        print("4")
        cur = mysql.cursor()
        planets = read_planet_data(cur)
        cur = mysql.cursor()
        invitation_codes = read_invitation_codes(cur)
        mysql.commit()
        cur.close()
        message = chr(4) + " " + chr(5) + " " + chr(30) + " " + chr(31)
        return render_template('admin.html', 
                                users=users, 
                                planets=planets,
                                invitation_codes=invitation_codes,
                                message=message)
    else:
        return redirect(url_for('login_page'))

