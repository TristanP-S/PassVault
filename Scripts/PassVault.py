import sqlite3 #database/storage
from hashlib import sha256 #hahses (encryption)
#MARK: Global Variables / Launch Statements
#sets master password, and sets up password prompt
masterPass = "123"
passPrompt = raw_input("Enter Password :-")
#while master password has failed to have been input (goes past when it finds password)
while masterPass != passPrompt:
    if masterPass != passPrompt:
        print("Invalid Password\n")
        break
if masterPass == passPrompt: #connects to database on device
    print("Welcome Back :)\nLoading...")
    passBase = sqlite3.connect('pass_manager.db')
#MARK: functions (python stores these for use in code below it)
#makes a password and encodes it
def create_password(pass_key, service, admin_pass):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8') + pass_key.encode('utf-8')).hexdigest()[
           :15]

#gets decryption/hex key using admin password
def get_hex_key(admin_pass, service):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

#gets password stored at location mentioned
def get_password(admin_pass, service):
    secret_key = get_hex_key(admin_pass, service)
    cursor = passBase.execute("SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')

    file_string = ""
    for row in cursor:
        file_string = row[0]
    return create_password(file_string, service, admin_pass)

#creates a password
def add_password(service, admin_pass):
    secret_key = get_hex_key(admin_pass, service)
    command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' % ('"' + secret_key + '"')
    passBase.execute(command)
    passBase.commit()
    return create_password(secret_key, service, admin_pass)
#deltes a password

#MARK: Main Code
if masterPass == passPrompt: #if password was entered properly (and db has loaded)
    try: #attempts to make a new 'table' called 'keys' for storage if one doesn't exist on device
        passBase.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
        print("Your PassSafe has been created!\nWhat do you want to do with it?")
    except: #if the attempt fails (table has already been made)
        print("You have a PassSafe, What do you want to do with it?")

    while True: #while password is correct (user hasn't restarted/closed the program)
        print("\n" + "*" * 15)
        print("Please note the names passwords are stored under are NOT case sensitive.")
        print("Also note, passwords are automatically generated for any given string, but aren't stored unless told to.")
        print("Commands(Enter command with \"\" to use or the program will crash):")
        print("1: Generate and Store a New Password")
        print("2: View Stored Password with a Certain Name")
        print("3: Delete Stored Password with a Certain Name")
        print("4: Quit This Program")
        print("*" * 15)
        input_ = raw_input("Input Command :-")

        if input_ == "4":
            break
        elif input_ == "1":
            service = raw_input("What should this password be stored under?\n")
            try:
                print("\n" + service.capitalize() + " password created:\n" + add_password(service, masterPass))
            except:
                print("There is already a password stored under this name, please delete it first.")
        elif input_ == "2":
            service = raw_input("What password do you want to check?\n")
            print("\n" + service.capitalize() + " password:\n" + get_password(masterPass, service))
        elif input_ == "3":
            try:
                service = raw_input("What password do you want to delete?\n")
            except:
                print("There is no password stored under this name.")
        else:
            print("\'" + input_ + "\'" + " is not a command")