from baseObject import baseObject
from user import user
import uifunctions


me = user()

import getpass



while len(me.data) != 1:
    
    email = raw_input("Enter email\n")
    mypass = getpass.getpass("Please enter your password:\n")

    me.tryLogin(email,mypass)

    if len(me.data) == 1:
        print "login ok - Hello" + me.data[0]['fname']
        
    else:
        print "login failed, please try again\n" 

s = uifunctions.makeMenu(['Users','Products','Exit'],'Enter a choice',True)
if s == 0:
    print "User screen"
elif s == 1:
    print "Product screen"
elif s == 2:
    print "Goodbye."
    exit()