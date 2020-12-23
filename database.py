from flask import Flask, render_template, redirect, request, url_for, session
import MySQLdb
from helper import verify_password

#app = Flask(__name__)


#mysql = MySQLdb.connect(host="Exodus2200.mysql.pythonanywhere-services.com", user="Exodus2200", passwd="Excalibur_01", db="Exodus2200$exodus2200")

#cur = mysql.cursor()

def create_tables(cur):
    
    #s = cur.execute('''CREATE TABLE IF NOT EXISTS TEST (id INT, name VARCHAR(20))''')
    #s = cur.execute('''DROP TABLE Users''')
    #s = cur.execute('''DROP TABLE Launches''')
    #s = cur.execute('''DROP TABLE Reports''')
    print("----------------------------------------------------")
    
    s = cur.execute('''CREATE TABLE IF NOT EXISTS Users (   user_id INT NOT NULL AUTO_INCREMENT, 
                                                            name VARCHAR(255),
                                                            username VARCHAR(32),
                                                            password VARCHAR(255),
                                                            date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                            invitation_code VARCHAR(32),
                                                            level INT NOT NULL DEFAULT 0,
                                                            found TEXT NOT NULL,
                                                            state VARCHAR(32) DEFAULT 'clear',
                                                            last_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                                            PRIMARY KEY (user_id) 
                                                            )''')

    """                                                            
    #s = cur.execute('''CREATE TABLE IF NOT EXISTS Planets ( planet_id INT NOT NULL, 
                                                            name VARCHAR(50),
                                                            x_pos INT,
                                                            y_pos INT,
                                                            z_pos INT,
                                                            url VARCHAR(255),
                                                            message VARCHAR(255),
                                                            PRIMARY KEY (planet_id) 
                                                            )''')
    
    #s = cur.execute('''CREATE TABLE IF NOT EXISTS Planets (id INT, name VARCHAR(20))''')
    #s = cur.execute('''CREATE TABLE IF NOT EXISTS State (id INT, name VARCHAR(20))''')

    """
    #cur.execute('''CREATE TABLE IF NOT EXISTS Invitation_codes(id INT, code VARCHAR(20), times_used INT)''')

    s = cur.execute('''CREATE TABLE IF NOT EXISTS Launches ( launch_id INT NOT NULL AUTO_INCREMENT,
                                                            user_id INT,
                                                            x_desto INT,
                                                            y_desto INT,
                                                            z_desto INT,
                                                            launch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                                            active BOOLEAN,
                                                            PRIMARY KEY (launch_id)
                                                        );''')
    
    s = cur.execute('''CREATE TABLE IF NOT EXISTS Reports ( report_id INT NOT NULL AUTO_INCREMENT,
                                                            user_id INT,
                                                            x_desto INT,
                                                            y_desto INT,
                                                            z_desto INT,
                                                            dist_from_nearest INT,
                                                            PRIMARY KEY (report_id)
                                                        );''')

    return

def add_test_data(cur):
    cur.execute('''TRUNCATE TABLE Users''')
    cur.execute('''INSERT INTO Users (name, username, password, invitation_code, found, level ) VALUES ("Alex van Winkel", "alexicoo", "1234", "TEST-001", "00000000", 0)''')
    cur.execute('''INSERT INTO Users (name, username, password, invitation_code, found, level ) VALUES ("Peter de Wit", "peter", "1234", "TEST-001", "00000000", 0)''')
    #cur.execute('''INSERT INTO Invitation_codes (id, code, times_used) VALUES (0, "INIT001", 0)''')
    cur.connection.commit()

    return

def add_planet_data(cur):
    s = cur.execute('''INSERT INTO Planets (planet_id, name, x_pos, y_pos, z_pos, url, message ) VALUES ( 0, "Tygross", -234, 877, 32, "Hx78Ah1u", "We have hacked your system")''')
    cur.connection.commit()

    return

def add_user(cur, name, username, password, invitation_code, level):
    found = "00000000"
    s = cur.execute('''INSERT INTO Users (name, username, password, invitation_code, found, level ) VALUES (%s, %s, %s, %s, %s, %s)''', (name, username, password, invitation_code, found, level ))
    cur.connection.commit()

    return

def read_user_data(cur):
    cur.execute('''SELECT * FROM Users''')
    records = cur.fetchall()
    return records

def read_planet_data(cur):
    cur.execute('''SELECT * FROM Planets''')
    records = cur.fetchall()
    return records

def read_invitation_codes(cur):
    cur.execute('''SELECT * FROM Invitation_codes''')
    records = cur.fetchall()
    return records

def check_credentials(username, password, cur):
    user_data = read_user_data(cur)
    match = False
    hash = ""
    for row in user_data:
        usr_name = row[2]
        pssw_hash = row[3]
        if usr_name == username:
            print("*** MATCH FOUND! ***")
            match = True
            hash = pssw_hash
    
    return verify_password(pssw_hash, password)

def launch_probe(x,y,z,cur):
    x_int = int(x)
    y_int = int(y)
    z_int = int(z)
    user = session.get('user')
    active = True    

    s = cur.execute('''INSERT INTO Launches (user_id, x_desto, y_desto, z_desto, active) VALUES ( %s, %s, %s, %s, %s)''',(user, x, y, z, True))
    cur.connection.commit()

    return

def get_level(cur, usr):
    cur.execute('''SELECT * FROM Users where username=%s''', (usr,))
    records = cur.fetchall()
    print("level: ", records[0][6])
    return records[0][6]

def get_state(cur, usr):
    cur.execute('''SELECT * FROM Users where username=%s''', (usr,))
    records = cur.fetchall()
    print("State: ", records[0][8])
    return records[0][8]
