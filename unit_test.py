from baseObject import baseObject
from user import user


#print u.fns
'''
newRow = {'fname':'John','lname':'Smith','email':'c@c.com'}

u.addRow(newRow)

print u.pk

if u.verify_new():
    print "Verify ok"
    u.insert()
else:
    print u.errors


newRow = {'name':'Tyler','lname':'Conlon','email':'c@c.com'}

u.addRow(newRow)
u.insert()

uid = u.data[0]['id']

u = user()
u.getById(uid)
u.data[0]['fname'] = "Bob"
u.update()

u = user()
u.getById(60)
u.data[0]['fname'] = "Bob"
u.update()

u = user()
u.deleteById(600)
u.getById(600)
u.getDataTable()


while True:
    u = user()

    un = raw_input("Enter email\n")
    pw = raw_input("Enter password\n")
    if u.tryLogin(un,pw):
        print "login ok"
    else:
        print "login failed"



u = user()
u.getById(600)
u.getDataTable()
'''


u = user()
u.getAll()
i=0
for usr in u.data:
    u.data[i]['email'] = "-"
    u.update(i)
    i+=1

#newRow = {'fname':'John','lname':'Smith','email':'a@a.com','pw':'123'}

#u.addRow(newRow)

#u.insert()


#u.verify_new()

#u.insert()
