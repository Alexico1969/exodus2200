import hashlib, binascii, os, datetime
 
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def time_left(launch_time):
    now = datetime.datetime.now()
    diff = now - launch_time
    minutes = int((diff.total_seconds())/60)
    print("minutes = " , minutes)
    return minutes

def random_username():
    temp_string = "guest_"
    now = datetime.datetime.now()
    temp_string += str(now)
    return temp_string

def random_password():
    now = datetime.datetime.now()
    output = str(now)
    return output