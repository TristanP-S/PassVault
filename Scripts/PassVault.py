import sqlite3 #database/storage
from hashlib import sha256 #hahses (encryption)
#MARK: Global Variables / Launch Statements
#sets master password, and sets up password prompt
masterPass = "123"
passPrompt = input("Enter Password :-")
#while master password has failed to have been input (goes past when it finds password)
while masterPass != passPrompt:
    if masterPass != passPrompt:
        print("Invalid Password\n")
        break
if masterPass == passPrompt: #connects to database on device
    print("Welcome Back :)\nLoading...")
    passBase = sqlite3.connect('pass_safe.db')
    passCursor = passBase.cursor()
#MARK: functions (python stores these for use in code below it)
#makes a password and encodes it
def create_password():
    return "1"

#gets decryption/hex key using admin password
def get_hex_key(admin_pass, service):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

#gets password stored at location mentioned
def get_password(admin_pass, service):
    secret_key = get_hex_key(admin_pass, service)
    passCursor.execute('SELECT * FROM keys WHERE value = {secret_key}')
    data = passCursor.fetchall()
    return data

#prints all data (will be deleted after testing)
def get_passwords():
    passCursor.execute('SELECT * FROM keys')
    data = passCursor.fetchall()
    print(data)
#creates a password
def add_password(admin_pass, service):
    secret_key = get_hex_key(admin_pass, service)
    pass_val = create_password()
    passCursor.execute("INSERT INTO keys (passkey, passval) VALUES ({secret_key}, {pass_val})")
    passBase.commit()
    return secret_key

#deletes a specified password
def del_password(admin_pass, service):
    secret_key = get_hex_key(admin_pass, service)
    passBase.cursor().execute("DELETE FROM keys WHERE passkey = (%s)" % (secret_key))
    passBase.commit()
    return

#deletes ALL passwords (by deleting the 'keys' table) except the primary key (not null)
def del_passwords():
    passBase.cursor().execute(("DELETE FROM keys"))
    passBase.commit()
    return
#MARK: Main Code
if masterPass == passPrompt: #if password was entered properly (and db has loaded)
    try: #attempts to make a new 'table' called 'keys' for storage if one doesn't exist on device
        passCursor.execute("CREATE TABLE IF NOT EXISTS keys(passkey TEXT, passval TEXT)")
        passBase.commit()
        print("Your PassSafe has been created!\nWhat do you want to do with it?")
    except: #if the attempt fails (table has already been made)
        print("You have a PassSafe, What do you want to do with it?")

    while True: #while password is correct (user hasn't restarted/closed the program)
        print("\n" + "*" * 15)
        print("Please note the names passwords are stored under are NOT case sensitive.")
        print("Commands(Enter command with \"\" to use or the program will crash):")
        print("1: Generate and Store a New Password")
        print("2: View Stored Password with a Certain Name")
        print("3: Delete Stored Password with a Certain Name")
        print("4: Delete ALL Stored Passwords")
        print("5: Quit This Program")
        print("*" * 15)
        input_ = input("Input Command :-")

        if input_ == "5":
            break
        elif input_ == "1":
            service = input("What should this password be stored under?\n")
            try:
                print("\n" + service.capitalize() + " password created:\n" + add_password(masterPass, service))
            except:
                print("There is already a password stored under this name, please delete it first.")
        elif input_ == "6":
            get_passwords()
        elif input_ == "2":
            service = input("What password do you want to check?\n")
            try:
                print("\n" + service.capitalize() + " password:\n" + get_password(masterPass, service))
            except:
                print("There is no password stored under this name, please make one first.")
        elif input_ == "3":
            try:
                service = input("What password do you want to delete?\n")
                del_password(masterPass, service)
                print("Password Deleted")
            except:
                print("There is no password stored under this name.")
        elif input_ == "4":
            input_2 = input("Are you sure you want to delete ALL your passwords? (Put Y for yes, N for no)")
            if input_2 == "Y":
                del_passwords()
                print("ALL stored passwords have been deleted")
            else:
                print("Stored passwords not deleted")
        else:
            print("\'" + input_ + "\'" + " is not a command")