from flask import Flask, render_template, redirect, request, url_for, session
import MySQLdb
from helper import verify_password

app = Flask(__name__)

mysql = MySQLdb.connect(host="Exodus2200.mysql.pythonanywhere-services.com", user="Exodus2200", passwd="Excalibur_01", db="Exodus2200$exodus2200")

def create_tables(cur):
    
    #s = cur.execute('''CREATE TABLE IF NOT EXISTS TEST (id INT, name VARCHAR(20))''')
    s = cur.execute('''DROP TABLE Users''')
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

    return

def add_test_data(cur):
    cur.execute('''TRUNCATE TABLE Users''')
    cur.execute('''INSERT INTO Users (name, username, password, invitation_code, found, level ) VALUES ("Alex van Winkel", "alexicoo", "1234", "TEST-001", "00000000", 0)''')
    cur.execute('''INSERT INTO Users (name, username, password, invitation_code, found, level ) VALUES ("Peter de Wit", "peter", "1234", "TEST-001", "00000000", 0)''')
    #cur.execute('''INSERT INTO Invitation_codes (id, code, times_used) VALUES (0, "INIT001", 0)''')
    mysql.commit()
    return

def add_planet_data(cur):
    s = cur.execute('''INSERT INTO Planets (planet_id, name, x_pos, y_pos, z_pos, url, message ) VALUES ( 0, "Tygross", -234, 877, 32, "Hx78Ah1u", "We have hacked your system")''')
    mysql.commit()
    return

def add_user(cur, name, username, password, invitation_code, level):
    found = "00000000"
    s = cur.execute('''INSERT INTO Users (name, username, password, invitation_code, found, level ) VALUES (%s, %s, %s, %s, %s, %s)''', (name, username, password, invitation_code, found, level ))
    mysql.commit()
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
    print("username: ", username)
    print("password: ", username)
    print("------------------------")
    print("usr_name: ", usr_name)
    print("pssw_hash", pssw_hash)
    print("password", password)
    print("------------------------")
    print("verified : ", verify_password(pssw_hash, password))
    return verify_password(pssw_hash, password)

    
