from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL
from database import create_tables, add_test_data, read_user_data, read_planet_data, add_user, add_planet_data
from database import read_invitation_codes, check_credentials, launch_probe, get_level, get_state, change_state
from database import get_time,  closest_planet, create_report, report_list, get_user_planets
import datetime
from helper import hash_password, verify_password, time_left

app = Flask(__name__)
app.secret_key = 'super secret key2'

app.config['MYSQL_USER'] = "Exodus2200"
app.config['MYSQL_PASSWORD'] = "Excalibur_01"
app.config['MYSQL_HOST'] = "Exodus2200.mysql.pythonanywhere-services.com"
app.config['MYSQL_DB'] = "Exodus2200$exodus2200"


if __name__ == '__main__':
    app.run()
    
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    if session.get('user'):
        cur = mysql.connection.cursor()
        user = session.get('user')
        state = session.get('state') #options : clear, launched, ... , ... 
        planets = get_user_planets(cur, user)
        time = 0
        if state:
            if state == 'launched':
                time = time_left(get_time(cur))
                if time <= 0:
                    print("landed")
                    change_state(cur, user, "landed")
        else:
            state = 'error'

        message = "All systems are go"

        if request.method == "POST":
            if request.form.get("L") == "logout":
                session.clear()
                return redirect(url_for('login_page'))
            elif request.form.get("action") == "launch":
                return redirect(url_for('launch'))
            elif request.form.get("action") == "read":
                time = time_left(get_time(cur))
                if time <= 0:
                    message = closest_planet(cur, user)
                    create_report(cur, user)
                    change_state(cur, user, "clear")
                    return render_template("message.html", message=message, goto="/")
                else:
                    message = "Probe is still on it's way..."
                    return render_template("message.html", message=message, goto="/")
            elif request.form.get("action") == "reports":
                print("Going to route REPORTS")
                return redirect(url_for('report'))
            else:
                output = request.form.get("action")
                print(output)
            return render_template('index.html',  message=message)
        else:
            message = "All systems operational"
            message = "Time var = " + str(time)
            return render_template('index.html',  message=message, user=user, state=state + "()", time=time, planets=planets)
    else:
        return redirect(url_for('login_page'))

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    message = ""
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        if request.form.get("R") == "register":
            return redirect(url_for('register'))
        else:
            message = "R is : " + str(request.form.get("R"))

        username = request.form['username']
        password = request.form['password']
        if username == "alex" and password == "csgo":
            session['logged_in'] = True
            session['admin'] = True
            session['user'] = username
            return redirect(url_for('home'))
        elif check_credentials(username, password, cur):
            message = "You are logged in as " + str(username)
            session['logged_in'] = True
            session['admin'] = False
            session['user'] = username
            print("## CHECKPOINT CHARLIE ##")
            session['level'] = get_level(cur, username)
            session['state'] = get_state(cur, username)
            cur.close()
            return render_template("message.html", message=message, goto="/")
        else:
            cur.close()
            message="username unknown or wrong password"


    return render_template("login.html", message=message)


@app.route("/register", methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST':
        
        cur = mysql.connection.cursor()
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

    if session.get('admin'):
        cur = mysql.connection.cursor()
        #create_tables(cur)
        #add_test_data(cur)
        users = read_user_data(cur)
        planets = read_planet_data(cur)
        invitation_codes = read_invitation_codes(cur)
        message = chr(4) + " " + chr(5) + " " + chr(30) + " " + chr(31)
        return render_template('admin.html', 
                                users=users, 
                                planets=planets,
                                invitation_codes=invitation_codes,
                                message=message)
    else:
        return redirect(url_for('login_page'))

@app.route("/launch", methods=['GET', 'POST'])        
def launch():

    if session.get('user') and session.get('state') == 'clear':
        message="Right : '023', '-821'  ; Wrong : '0', '-11', '1234'"
        user = session.get('user')
        if request.method == "POST":
            if request.form.get("L") == "logout":
                session.clear()
                return redirect(url_for('login_page'))
            elif request.form.get("x_desto") and request.form.get("y_desto") and request.form.get("z_desto"):
                cur = mysql.connection.cursor()
                x = request.form.get("x_desto")
                y = request.form.get("y_desto")
                z = request.form.get("z_desto")
                launch_probe(x,y,z,cur)
                message = "Destination set !           (" + x + "," + y + "," + z + ")"
                change_state(cur, user, "launched")
                return render_template("message.html", message=message, goto="/")
            else:
                message = "Missing coordinates"
                
            return render_template('launch.html', user=user, message=message)
        
        
        return render_template('launch.html', user=user, message=message)
    else:
        return redirect(url_for('login_page'))


@app.route("/report", methods=['GET', 'POST'])        
def report():
    if session.get('user'):
        
        print("route Report ---- activated")
        message = "message"
        cur = mysql.connection.cursor()
        user = session.get('user')
        #state = session.get('state') #options : clear, launched, ... , ... 
        launches = report_list(cur, user)

        if request.method == "POST":
            if request.form.get("action") == "back":
                return redirect(url_for('home'))

        return render_template('reports.html', message=message, user=user, state="clear()", time=0, launches=launches)
    else:
        return redirect(url_for('login_page'))

