from colorama import init
init()
import mysql.connector
import random
from colorama import Fore, Back, Style
from prettytable import PrettyTable
import matplotlib.pyplot as plt

uname_logged = ""
uname = "a"

lst = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "@", "#", "%", "&" "*", "!"]
mst_pw = ["dS2d", "Jj8d", "d4gF", "kP9d", "08dD", "pbS8", "Bs8a", "pd8f", "agr8", "jj9a", "hai2", "0sof", "snvo", "Opa7", "u6sB", "sPa8", "Pa6s", "ncD6", "tY8a", "Kda6", "0Oda", "ns9p", "Nui6", "dAc7", "sOc4", "pabc", "Bua7", "hFa4", "Va8b", "dixS", "Mqz2", "6Ytb", "lL1I", "xP43", "1mN9", "g8j3", "Ux7T", "Bd7z", "Gs6x", "jC5a", "gccS", "on7S", "pc7n", "kB7z", "jFc6", "ka0X", "b7st", "s9V6", "oP8b", "Z7ab", "0Asl", "l7zv", "paC5", "ms6Y", "Px8N", "hS57", "lB7z", "e9Nt", "xZy9", "3pLn", "Ghb7", "nY6s", "Jsu6", "p0cY", "Mi8X", "x7Hv", "bc7D", "lkH6"]
hash_pw = ["uC7w", "aD8e", "d9Kl", "vL8R", "bO6P", "g0Jm", "V5ch", "H7bs", "rU5b", "Fu5N", "dK4A", "Dr6P", "D9pL", "kO6D", "V7pD", "Ap0D", "e6Aj", "Uh6f", "jF8n", "fDb7", "dPA7", "yD5M", "Su3q", "pR5w", "Fy8M", "B8fM", "qO7n", "fI6n", "mI7n", "dtU4", "sdI4", "pnF8", "A1dP", "ha3M", "dKh8", "Ah4S", "MjL8", "bKy8", "dK8A", "sK5X", "fw7S", "U8vT", "vN6n", "dkL4", "qwE7", "elM4", "4SgJ", "rjL7", "jne3", "kw5M", "mkL6", "dS7G", "Ded7", "mKc7", "vsM8", "i5Dh", "eNiR", "sC7b", "e4Cm", "dNu2", "A2iK", "dMi1", "hxG6", "xH7s", "z0Bx", "f7Bh", "d98B", "dH6x"]

log_file = open("log.txt", "a")
log_file.write("\n\n\nSESSION START\nThis is the log file for your Password Manager.\nPlease do not delete this file, do not. And when I say do not, don't even think about it.\n\n")

mydb = mysql.connector.connect (host="localhost", user="root", password="qwerty")
mycursor = mydb.cursor()
mycursor.execute ("CREATE DATABASE IF NOT EXISTS pwmngr")
mycursor.execute ("USE pwmngr")
mycursor.execute ("CREATE TABLE IF NOT EXISTS users (userid VARCHAR(64), mst_hash VARCHAR(256))")


###################################################################

def mst_to_hash(txt):
    x = list(txt)
    mst_hash = ""
    for i in x:
        ltr = lst.index(i)
        mst_hash += mst_pw[ltr]
    return mst_hash

###################################################################

def pw_to_hash(txt):
    x = list(txt)
    pw_hash = ""
    for i in x:
        ltr = lst.index(i)
        pw_hash += hash_pw[ltr]
    return pw_hash

###################################################################

def hash_to_pw(txt):
    hash_ltr = []
    decrypt_pw = ""
    for i in range(0, len(txt), 4):
        hash_ltr.append(txt[i:i+4])
    for hs_ltr in hash_ltr:
        ltr = hash_pw.index(hs_ltr)
        decrypt_pw += lst[ltr]
    return decrypt_pw

###################################################################

def login():
    global uname
    global uname_logged
    chk_u = 0
    chk_p = 0
    uname_logged = ""
    while (True):
        uname = input("Enter " + Fore.GREEN + "username" + Fore.RESET + " (Type " + Fore.RED + "EXIT" + Fore.RESET + " to exit): ")
        mycursor.execute ("SELECT userid FROM users")
        chk_user = mycursor.fetchall()
        if uname != "EXIT" and uname != "exit":
            for chk_usr in chk_user:
                if uname in chk_usr:
                    chk_u = 1
                    log_file_write = "User " + uname + " is trying to log in.\n"
                    log_file.write(log_file_write)
                    break
        else:
            break
        if chk_u != 1:
            log_file_write = "Wrong username " + uname + " tried to log in.\n"
            log_file.write(log_file_write)
            print (Back.RED + Fore.WHITE + "Username doesn't exists." + Style.RESET_ALL)
        else:
            break
    if chk_u == 1:
        def ent_pw():
            nonlocal chk_p
            try_again_pw = "N"
            mst_password = input("Enter password: ")
            mst_pw_check = mst_to_hash(mst_password)
            mycursor.execute ("SELECT mst_hash FROM users WHERE userid = '" + uname + "'")
            chk_passwd = mycursor.fetchall()
            for chk_pw in chk_passwd:
                if mst_pw_check in chk_pw:
                    chk_p = 1
                    log_file_write = "User " + uname + " logged in successfully\n"
                    log_file.write(log_file_write)
                else:
                    log_file_write = "Wrong password for user " + uname + " was typed.\n"
                    log_file.write(log_file_write)
                    try_again_pw = input("Wrong Password, try again? (Y/N): ")
            if try_again_pw == "Y" or try_again_pw == "y":
                ent_pw()
        ent_pw()
    if chk_u == 1 and chk_p == 1:
        uname_logged = uname
        chk_u = 0
        chk_p = 0
        print ("Welcome ", uname_logged)

###################################################################

def create_user():
    while (True):
        usr_avail = 1
        new_uname = input("Enter your new " + Fore.GREEN + "username" + Fore.RESET + ": ")
        mycursor.execute("SHOW TABLES")
        chk_userid = mycursor.fetchall()
        for chk_usr in chk_userid:
            if new_uname in chk_usr:
                usr_avail = 0
        if new_uname == "EXIT" or new_uname == "exit":
            usr_avail = 0
        if usr_avail == 1:
            log_file_write = "A new user " + new_uname + " was created now.\n"
            log_file.write(log_file_write)
            new_pw = input("Please enter your new " + Fore.GREEN + "password" + Fore.RESET + ": ")
            f = new_uname
            mycursor.execute ("CREATE TABLE " + f + "(sitename varchar(64), website varchar(128), username varchar(64), password varchar(256))")
            p = mst_to_hash(new_pw)
            mycursor.execute ("INSERT INTO users VALUES ('" + f + "', '" + p + "')")
            mydb.commit()
            print (Back.BLUE + "Hurray! You have successfully created your account." + Back.RESET)
            break
        else:
            print (Back.RED + Fore.BLACK + "Username exists. Please use some other username." + Style.RESET_ALL)

###################################################################

def edit_acc_pw():
    if uname != uname_logged:
        login()
    if uname_logged == uname:
        password_new = input("Enter your new " + Fore.GREEN + "password" + Fore.RESET + ": ")
        password_new_enc = mst_to_hash(password_new)
        exec = "UPDATE users SET mst_hash = '" + password_new_enc + "'"
        mycursor.execute(exec)
        mydb.commit()
        print (Back.BLUE + "Your password has been successfully changed." + Style.RESET_ALL)
        log_file_write = "The user " + uname_logged + " changed their password.\n"
        log_file.write(log_file_write)

###################################################################

def view_pw():
    if uname_logged == uname:
        print(Fore.BLUE + "+-----------------------------------------------------------+")
        print("|-----------------------------------------------------------|")
        print("|---", uname_logged.center(51), "---|")
        print("|===========================================================|")
        print("|-----------------------------------------------------------|")
        print("|-------------------   YOUR PASSWORDS   --------------------|")
        print("|===========================================================|")
        print("|-----------------------------------------------------------|")
        print("+-----------------------------------------------------------+" + Fore.RESET)


        def show_pw():
            exec = "SELECT * FROM " + uname_logged
            mycursor.execute(exec)
            show_py_table = mycursor.fetchall()
            pty_tb = PrettyTable()

            pty_tb.field_names = ["SITE NAME", "WEBSITE URL", "USERNAME", "PASSWORD"]

            for i in show_py_table:
                pw_decrypt = hash_to_pw(i[3])
                pty_tb.add_row([i[0], i[1], i[2], pw_decrypt])
            
            print (pty_tb)
            log_file_write = "The user " + uname_logged + " checked their passwords.\n"
            log_file.write(log_file_write)
            

        def add_pw():
            stnm = input("Enter the " + Fore.GREEN + "SITE NAME" + Fore.RESET + " (eg. Gmail): ")
            wbst = input("Enter the " + Fore.GREEN + "WEBSITE URL" + Fore.RESET + " (eg. mail.google.com): ")
            usrnm_a = input("Enter your " + Fore.GREEN + "USERNAME" + Fore.RESET + " of your account (eg. username@example.com): ")
            pass_pw = input("Enter the " + Fore.GREEN + "PASSWORD" + Fore.RESET + ": ")
            pass_pw_enc = pw_to_hash(pass_pw)
            exc = "INSERT INTO " + uname_logged + " VALUES ('" + stnm + "', '" + wbst + "', '" + usrnm_a + "', '" + pass_pw_enc + "')"
            mycursor.execute(exc)
            mydb.commit()
            log_file_write = "The user " + uname_logged + " added a password to their database.\n"
            log_file.write(log_file_write)

        def edit_pw():
            while (True):
                print ("\n1. USERNAME\n2. PASSWORD\n3. " + Fore.RED + "BACK" + Fore.RESET)
                edit_req = input("What do you want to edit? (1/2/3): ")
                if edit_req == "1":
                    stnm = input("Enter your " + Fore.GREEN + "SITENAME" + Fore.RESET + " (eg. Gmail): ")
                    usrnm_edit = input("Enter your " + Fore.GREEN + "OLD USERNAME" + Fore.RESET + ": ")
                    usrnm_edit_n = input("Enter your " + Fore.GREEN + "NEW USERNAME" + Fore.RESET + ": ")
                    exec = "UPDATE " + uname_logged  + " SET username = '" + usrnm_edit_n + "' WHERE username = '" + usrnm_edit + "' and sitename like '%" + stnm + "%'"
                    mycursor.execute(exec)
                    mydb.commit()
                    log_file_write = "The user " + uname_logged + " edited their username from " + usrnm_edit + " to " + usrnm_edit_n + ".\n"
                    log_file.write(log_file_write)
                elif edit_req == "2":
                    stnm = input("Enter your " + Fore.GREEN + "SITENAME" + Fore.RESET + " (eg. Gmail): ")
                    usrnm_edit = input("Enter your " + Fore.GREEN + "USERNAME" + Fore.RESET + ": ")
                    pw_edit_n_d = input("Enter your " + Fore.GREEN + "NEW PASSWORD" + Fore.RESET + ": ")
                    pw_edit_n = pw_to_hash(pw_edit_n_d)
                    exec = "UPDATE " + uname_logged + " SET password = '" + pw_edit_n + "' WHERE username = '" + usrnm_edit + "' and sitename like '%" + stnm + "%'"
                    mycursor.execute(exec)
                    mydb.commit()
                    log_file_write = "The user " + uname_logged + " changed their password for " + usrnm_edit + " on " + stnm + ".\n"
                    log_file.write(log_file_write)
                elif edit_req == "3":
                    break
                else:
                    print (Back.RED + "Sorry couldn't catch that." + Back.RESET)

        def srch_pw():
            while (True):
                print ("\n1. SEARCH WITH SITENAME\n2. SEARCH WITH USERNAME\n3. SEARCH WITH SITENAME AND USERNAME\n4. " + Fore.RED + "BACK" + Fore.RESET)
                srch_req = input("Enter your " + Fore.GREEN + "search type" + Fore.RESET + " (1/2/3/4): ")
                if srch_req == "1":
                    stnm_src = input("Enter your " + Fore.GREEN + "SITENAME" + Fore.RESET + " (eg. Gmail): ")
                    exec = "SELECT * FROM " + uname_logged + " WHERE sitename like '%" + stnm_src + "%'"
                    mycursor.execute(exec)
                    show_py_table = mycursor.fetchall()
                    pty_tb = PrettyTable()

                    pty_tb.field_names = ["SITE NAME", "WEBSITE URL", "USERNAME", "PASSWORD"]

                    for i in show_py_table:
                        pw_decrypt = hash_to_pw(i[3])
                        pty_tb.add_row([i[0], i[1], i[2], pw_decrypt])
                    print (pty_tb)
                    log_file_write = "The user " + uname_logged + " searched on " + stnm_src + ".\n"
                    log_file.write(log_file_write)
                elif srch_req == "2":
                    usrnm_src = input("Enter your " + Fore.GREEN + "USERNAME" + Fore.RESET + ": ")
                    exec = "SELECT * FROM " + uname_logged + " WHERE username like '%" + usrnm_src + "%'"
                    mycursor.execute(exec)
                    show_py_table = mycursor.fetchall()
                    pty_tb = PrettyTable()

                    pty_tb.field_names = ["SITE NAME", "WEBSITE URL", "USERNAME", "PASSWORD"]

                    for i in show_py_table:
                        pw_decrypt = hash_to_pw(i[3])
                        pty_tb.add_row([i[0], i[1], i[2], pw_decrypt])
            
                    print (pty_tb)
                    log_file_write = "The user " + uname_logged + " searched for " + usrnm_src + ".\n"
                    log_file.write(log_file_write)
                elif srch_req == "3":
                    stnm_src = input("Enter your " + Fore.GREEN + "SITENAME" + Fore.RESET + " (eg. Gmail): ")
                    usrnm_src = input("Enter your " + Fore.GREEN + "USERNAME" + Fore.RESET + ": ")
                    exec = "SELECT * FROM " + uname_logged + " WHERE sitename like '%" + stnm_src + "%' and username like '%" + usrnm_src + "%'"
                    mycursor.execute(exec)
                    show_py_table = mycursor.fetchall()
                    pty_tb = PrettyTable()

                    pty_tb.field_names = ["SITE NAME", "WEBSITE URL", "USERNAME", "PASSWORD"]

                    for i in show_py_table:
                        pw_decrypt = hash_to_pw(i[3])
                        pty_tb.add_row([i[0], i[1], i[2], pw_decrypt])
            
                    print (pty_tb)
                    log_file_write = "The user " + uname_logged + " searched for " + usrnm_src + " on " + stnm_src + ".\n"
                    log_file.write(log_file_write)
                elif srch_req == "4":
                    break
                else:
                    print ("Sorry couldn't catch that.")

        def graph():
            exec = "SELECT * FROM " + uname_logged
            mycursor.execute(exec)
            show_py_table = mycursor.fetchall()
            st_nm_l = {}
            for i in show_py_table:
                st_nm = i[0]
                if st_nm in st_nm_l:
                    st_nm_l[st_nm] += 1
                else:
                    st_nm_l[st_nm] = 1

            g_dic = st_nm_l
            
            labels = []
            sizes = []
            for i in g_dic:
                labels.append(i)
                x = g_dic.get(i)
                sizes.append(x)



            g_dic_len = len(g_dic)
            g_dic_len_a = g_dic_len
            color = ["red", "gold", "greenyellow", 'cyan', 'mediumblue', 'darkviolet', 'magenta']
            color_ran_old = "hello"
            colors = []
            while g_dic_len > 0:
                color_ran = random.choice(color)
                if color_ran != color_ran_old:
                    colors.append(color_ran)
                    g_dic_len -= 1
                    color_ran_old = color_ran

            explode = []
            for i in range(0, g_dic_len_a):
                x = 0.03
                explode.append(x)



            plt.pie(sizes,explode=explode,labels=labels,colors=colors,shadow=True)
            plt.axis('equal')
            plt.show()

        
        def del_pw():
            stnm_del = input("Enter your SITENAME (eg. Gmail): ")
            usrnm_del = input("Enter your USERNAME: ")
            exec = "DELETE FROM " + uname_logged + " WHERE sitename = '" + stnm_del + "' AND username = '" + usrnm_del + "'"
            mycursor.execute(exec)
            mydb.commit()
            log_file_write = "The user " + uname_logged + " deleted their record for " + usrnm_del + " on " + stnm_del + ".\n"
            log_file.write(log_file_write)


        vp_a = 1
        vp_b = 2
        while (vp_b > vp_a):
            if uname_logged == uname:
                view_l = "LOG IN TO ANOTHER ACCOUNT"
            else:
                view_l = "LOG IN"
            
            def ent_req_d():
                nonlocal vp_a
                print("\n1.", view_l)
                print("2. SHOW PASSWORDS\n3. ADD ANOTHER PASSWORD\n4. EDIT A PASSWORD\n5. SEARCH FOR A PASSWORD\n6. SHOW GRAPH OF NUMBER OF ACCOUNTS\n7. DELETE A PASSWORD\n8. " + Fore.RED + "BACK" + Fore.RESET)

                ent_req = input("Enter your " + Fore.GREEN + "request (1/2/3/4/5/6/7)" + Fore.RESET + ": ")
                if ent_req == "1":
                    login()
                elif ent_req == "2":
                    show_pw()
                elif ent_req == "3":
                    add_pw()
                elif ent_req == "4":
                    edit_pw()
                elif ent_req == "5":
                    srch_pw()
                elif ent_req == "6":
                    graph()
                elif ent_req == "7":
                    del_pw()
                elif ent_req == '8':
                    vp_a = 3
                else:
                    print (Back.RED + "Sorry couldn't catch that." + Back.RESET)
                    ent_req_d()
            ent_req_d()
    else:
        print(Back.RED + "Please Log in first." + Back.RESET)

###################################################################

def show_log():
    global log_file
    log_file.close()
    log_file = open("log.txt", "r")
    log_show = log_file.read()
    print (log_show)
    log_file.close()
    log_file = open("log.txt", "a")
    log_file_write = "The log file was read.\n"
    log_file.write(log_file_write)

###################################################################

def create_pw():
    lower = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    upper = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "@", "#", "%", "&", "*", "!"]
    pwlenrand = [10, 11, 12, 13, 14, 15, 16, 17, 18]
    password = ""
    diffi = int(input("Enter " + Fore.GREEN + "level 1/2/3" + Fore.RESET + ": "))

    if diffi == 1:
        diff = ["l"]
    elif diffi == 2:
        diff = ["l", "u"]
    elif diffi == 3:
        diff = ["l", "u", "d"]

        
    leng = int(input("Enter the " + Fore.GREEN + "length of the password" + Fore.RESET + " (0 for random): "))
    if leng == 0:
        leng = random.choice(pwlenrand)

    for i in range(1, leng+1):
        diffic = random.choice(diff)
        if diffic == "l":
            x = random.choice(lower)
        elif diffic == "u":
            x = random.choice(upper)
        elif diffic == "d":
            x = random.choice(digits)
        password += x
    print ("Your password is " + Fore.GREEN + password + Fore.RESET)
    log_file_write = "A password was create for an user.\n"
    log_file.write(log_file_write)

###################################################################

while (True):
    print(Fore.BLUE + "+-----------------------------------------------------------+")
    print("|-----------------------------------------------------------|")
    print("|----------------------   PWMNGR   -------------------------|")
    print("|                     ==============                        |")
    print("|-----------------------------------------------------------|")
    print("|----------------   MY PASSWORD MANAGER   ------------------|")
    print("|           ===================================             |")
    print("|-----------------------------------------------------------|")
    print("+-----------------------------------------------------------+" + Fore.RESET)

    if uname_logged == uname:
        view_l = "LOG IN TO ANOTHER ACCOUNT"
    else:
        view_l = "LOG IN"
    print ("\n1.", view_l, "\n2. SIGN UP\n3. EDIT YOUR ACCOUNT PASSWORD\n4. MANAGE YOUR PASSWORDS\n5. CREATE A PASSWORD FOR YOU\n6. SHOW LOG FILE\n7. " + Fore.RED + "EXIT" + Fore.RESET)
    print ("\n")
    def ent_req_d():
        ent_req = input("Enter your " + Fore.GREEN + "request (1/2/3/4/5/6/7)" + Fore.RESET + ": ")
        print ("\n")
        if ent_req == "1":
            login()
        elif ent_req == "2":
            create_user()
        elif ent_req == "3":
            edit_acc_pw()
        elif ent_req == "4":
            view_pw()
        elif ent_req == "5":
            create_pw()
        elif ent_req == "6":
            show_log()
        elif ent_req == "7":
            print (Fore.BLUE + "BYE!" + Fore.RESET)
            exit()
        else:
            print (Back.RED + "Sorry couldn't catch that." + Back.RESET)
            ent_req_d()
    ent_req_d()

log_file_write = "\n\n\n"
log_file.write(log_file_write)
log_file.close()