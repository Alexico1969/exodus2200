from flask import Flask, render_template, redirect, request, url_for, session, Markup
import MySQLdb, time, datetime
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
    
    cur.execute('''CREATE TABLE IF NOT EXISTS Users (   user_id INT NOT NULL AUTO_INCREMENT, 
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
    cur.execute('''CREATE TABLE IF NOT EXISTS Planets ( planet_id INT NOT NULL, 
                                                            name VARCHAR(50),
                                                            x_pos INT,
                                                            y_pos INT,
                                                            z_pos INT,
                                                            url VARCHAR(255),
                                                            message VARCHAR(255),
                                                            PRIMARY KEY (planet_id) 
                                                            )''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS Planets (id INT, name VARCHAR(20))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS State (id INT, name VARCHAR(20))''')

    """
    #cur.execute('''CREATE TABLE IF NOT EXISTS Invitation_codes(id INT, code VARCHAR(20), times_used INT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Hints(hint_id INT NOT NULL AUTO_INCREMENT, hint VARCHAR(255), PRIMARY KEY (hint_id))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Launches ( launch_id INT NOT NULL AUTO_INCREMENT,
                                                            user_id INT,
                                                            x_desto INT,
                                                            y_desto INT,
                                                            z_desto INT,
                                                            launch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                                            active BOOLEAN,
                                                            PRIMARY KEY (launch_id)
                                                        );''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS Reports ( report_id INT NOT NULL AUTO_INCREMENT,
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
    cur.execute('''INSERT INTO Users (name, username, password, invitation_code, found, level ) VALUES (%s, %s, %s, %s, %s, %s)''', (name, username, password, invitation_code, found, level ))
    cur.connection.commit()
    cur.execute('''SELECT * from Invitation_codes WHERE code=%s ORDER BY id DESC LIMIT 1''', ([invitation_code]))
    records = cur.fetchall()
    huidige_aantal = records[0][2]
    print(huidige_aantal)
    huidige_aantal += 1
    cur.execute('''UPDATE Invitation_codes SET times_used=%s WHERE code=%s''', (huidige_aantal, invitation_code))
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

def read_reports(cur):
    cur.execute('''SELECT * FROM Reports''')
    records = cur.fetchall()
    return records

def check_credentials(username, password, cur):
    user_data = read_user_data(cur)
    hash = ""
    for row in user_data:
        usr_name = row[2]
        pssw_hash = row[3]
        if usr_name == username:
            print("*** MATCH FOUND! ***")
            hash = pssw_hash
    
    return verify_password(hash, password)

def launch_probe(x,y,z,cur):
    user = user_id(cur,session.get('user'))
    cur.execute('''INSERT INTO Launches (user_id, x_desto, y_desto, z_desto, active) VALUES ( %s, %s, %s, %s, %s)''',(user, x, y, z, True))
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

def change_state(cur, user, new_state):
    print("*** function change_state ***")
    print("user: ", user)
    print("new_state: ", new_state)
    cur.execute('''UPDATE Users SET state=%s WHERE username=%s''', (new_state, user))
    cur.connection.commit()
    session['state'] = new_state
    return

def get_time(cur):
    print("*** function get_time ***")
    user = user_id(cur, session.get('user'))
    cur.execute('''SELECT * FROM Launches where user_id=%s ORDER BY launch_id DESC LIMIT 1''', (user,))
    records = cur.fetchall()
    if records:
        print("last launch: ", records[0][5])
        return records[0][5]
    else:
        print("no lauches for this user in DB")
        return 0

def user_id(cur, name):
    cur.execute('''SELECT * FROM Users where username=%s''', (name,))
    records = cur.fetchall()
    print("User_Id: ", records[0][0])
    return records[0][0]

def closest_planet(cur, user):
    usr_id = user_id(cur, user)
    coord_list = get_xyz(cur, usr_id)
    if coord_list == []:
        return 999999
    else:
        x = coord_list[0]
        y = coord_list[1]
        z = coord_list[2]
        print(" xyz = ", x, y, z)

        planets = []
        planets = get_planet_coords(cur)
        closest = 888888
        counter = 0
        found_planet = -1

        print("_________________________")

        print("x = ",x)
        print("y = ",y)
        print("z = ",z)

        print("_________________________")

        for planet in planets:
            xp = planet[0]
            yp = planet[1]
            zp = planet[2]

            distance =  ((x-xp)**2 + (y-yp)**2 + (z-zp)**2)**(0.5)
            if distance < closest:
                closest = distance
                if closest == 0:
                    planet_nr = counter
                    add_planet_found(cur, user, planet_nr)
                else:
                    print("xp = ",xp)
                    print("yp = ",yp)
                    print("zp = ",zp)
                    print("",)
                    
            counter += 1

        closest = int(closest)

        cur.execute('''INSERT INTO Reports (user_id, x_desto, y_desto, z_desto, dist_from_nearest) VALUES ( %s, %s, %s, %s, %s)''',(usr_id, x, y, z, distance))
        cur.connection.commit()
        print("-->  About to be deleted : All lauches with user id ", usr_id)
        cur.execute('''DELETE FROM Launches WHERE user_id = %s''',(usr_id,))
        cur.connection.commit()


        if closest == 0:
            name_found_planet = name_planet(cur, planet_nr)
            output = "You have found planet " + name_found_planet +  " !"
            return output
        else:
            return "Shortest distance to a planet = " + str(closest) + ".000 KM"

def get_xyz(cur, user):
    coord_list = []
    cur.execute('''SELECT * FROM Launches where user_id=%s ORDER BY launch_id DESC LIMIT 1''', (user,))
    records = cur.fetchall()
    #print("&&& records[0][2] : ", records[0][2])
    if records:
        coord_list.append(records[0][2])  # x
        coord_list.append(records[0][3])  # y
        coord_list.append(records[0][4])  # z
        print("launch coords: ", coord_list)
    else:
        print("no launches for this user in DB")
    
    return coord_list

def get_planet_coords(cur):
    planets = []
    cur.execute('''SELECT * FROM Planets ''')
    records = cur.fetchall()
    for record in records:
        x = record[2]
        y = record[3]
        z = record[4]
        planets.append([x,y,z])
    return planets

def name_planet(cur, found_planet):
    cur.execute('''SELECT * FROM Planets ''')
    records = cur.fetchall()
    name = records[found_planet][1]
    return name

def report_list(cur, user):

    id = user_id(cur, user)
    r_list = []

    cur.execute('''SELECT * FROM Reports ''')
    records = cur.fetchall()

    for record in records:
        if record[1] == id:
            temp_string = str(record[2]) + " / " + str(record[3]) + " / " + str(record[4])  + " <--> " + str(record[5]) + ".000 km"
            r_list.append(temp_string)

    return r_list

def get_user_planets(cur, user):
    
    id = user_id(cur, user)
    output = ""
    planets = []
    cur.execute('''SELECT * FROM Planets ''')
    records = cur.fetchall()
    for record in records:
        planets.append(record)
    f_string = found_string(cur, id)

    for index in range(8):
        pf = f_string[index]
        if pf == '1':
            output += '<p><a href="../static/' + planets[index][5] + '.html" target="_blank">' + planets[index][1] + '</a></p>'    

    
    output = Markup(output)   
    #output = Markup("<p>Tygross</p><p>Mycos</p>")
    return output

def add_planet_found(cur, user, planet_nr):

    id = user_id(cur, user)
    current_found = found_string(cur, id)
    new_found = ""
    for index in range(8):
        if index == planet_nr:
            new_found += "1"
        else:
            new_found += current_found[index]
    cur.execute('''UPDATE Users SET found=%s WHERE user_id=%s''', (new_found, id))
    cur.connection.commit()
    return

def found_string(cur, id):
    cur.execute('''SELECT * FROM Users WHERE user_id=%s''', (id,))
    records = cur.fetchall()
    f_string = records[0][7]
    return f_string

def reports_exist(cur, user):
    id = user_id(cur, user)

    cur.execute('''SELECT * FROM Reports WHERE user_id=%s''', (id,))
    records = cur.fetchone()

    if records == None:
        result = False
    else:
        result = True

    return result

def process_login(cur, user):
    id = user_id(cur, user)
    cur.execute('''SELECT * FROM Users WHERE user_id=%s''', (id,))
    records = cur.fetchall()
    last_login = str(records[0][9])
    ts = time.time()
    st = str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
    day_last = int(last_login[8:10])
    day_now = int(st[8:10])
    print("-->  DAY LAST  = ", day_last)
    print("-->  DAY NOW   = ", day_now)
    timespan = day_now - day_last
    print("-->  TIMESPAN  = ", timespan)
    cur.execute('''UPDATE Users SET last_time=%s WHERE user_id=%s''', (st, id))
    cur.connection.commit()
    return timespan

def insert_hint(cur, hint):
    cur.execute('''INSERT INTO Hints (hint) VALUES (%s)''', (hint,))
    cur.connection.commit()
    return

def get_hint(cur, index):
    cur.execute('''SELECT * FROM Hints''')
    records = cur.fetchall()
    hint = records[index][1]
    full_sentence = "After doing some research, your scientists came to the following conclusion : " + hint
    return full_sentence

def set_level(cur, user, level):
    id = user_id(cur, user)
    cur.execute('''UPDATE Users SET level=%s WHERE user_id=%s''', (level, id))
    cur.connection.commit()
    return

def purge_guests(cur):
    guest_ids = []    
    cur.execute('''SELECT user_id from Users WHERE name='guest' ''')
    records = cur.fetchall()
    print("*** Fetching guest id's")
    
    for r in records:
        guest_ids.append(r[0])
    print("guest id's :", guest_ids)
    print("*** purging guests ***")
    for id in guest_ids:
        cur.execute('''DELETE from Users WHERE user_id = %s''', (id,))
        cur.execute('''DELETE from Reports WHERE user_id = %s''', (id,))
    cur.connection.commit()

    

