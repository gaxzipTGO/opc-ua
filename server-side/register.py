import re
import sqlite3
import hashlib

def createUITableIfNotExists():
    with sqlite3.connect('db/opcua-credential.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS UserIdentity(username text PRIMARY KEY, password text NOT NULL)')
        conn.commit()
        cursor.close()
    # end with-as
# createUITableIfNotExists()

def insertNewRecord(username, password):
    with sqlite3.connect('db/opcua-credential.db') as conn:
        cursor = conn.cursor()
        hashed_password = hashlib.sha3_256(password.encode(encoding='UTF-8')).hexdigest()
        cursor.execute('INSERT INTO UserIdentity Values(?,?)', [username, hashed_password])
        conn.commit()
        cursor.close()
    # end with-as
# end insertNewRecord()

def isValidatedUsername(username):
    with sqlite3.connect('db/opcua-credential.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(username) FROM UserIdentity WHERE username=?', [username])
        is_existed = True if cursor.fetchone()[0] == 1 else False
        cursor.close()
    # end with-as

    if is_existed:
        print('Username already exists\n')
        return False
    else: return True
# end isValidatedUsername()

def isValidatedPassword(password):
    if len(password) < 10:
        print('Password must contain at least 10 characters\n')
        return False
    elif re.search(r'\d', password) is None:
        print('Password must contain at least 1 digit\n')
        return False
    elif re.search(r'[a-z]', password) is None:
        print('Password must contain at least 1 lower-case letter\n')
        return False
    elif re.search(r'[A-Z]', password) is None:
        print('Password must contain at least 1 upper-case letter\n')
        return False
    elif re.search(r'[ !"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]', password) is None:
        print('Password must contain at least 1 symbol\n')
        return False
    else: 
        password_second_time = input('Enter password again: ')
        if password != password_second_time:
            print('Password doesn\'t match!\n')
            return False
        else: return True
    # end if-elif-else
# end isValidatedPassword()

def register():
    # get a validated username/passowrd
    username = input('Enter username: ')
    while not isValidatedUsername(username): username = input('Enter username: ')
    password = input('Enter password: ')
    while not isValidatedPassword(password): password = input('Enter password: ')        
    # registration
    createUITableIfNotExists()
    insertNewRecord(username, password)
    print('Register successfully!')
# end register()

if __name__ == '__main__': register()