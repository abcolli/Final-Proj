from baseObject import baseObject
import pymysql
import hashlib
class user(baseObject):
    def __init__(self):
        tn = 'collins_customer2'
        pk = 'user_id'
        self.roleList = [['Customer','1'],['Employee','2']]
        
       
        self.setupObject(tn,pk)
    def verify_new(self,n=0):
        self.errors = []
        if self.data[n]['fname'] == '':
            self.errors.append("You must enter a first name.")
        if self.data[n]['lname'] == '':
            self.errors.append("You must enter a last name.")
        if self.data[n]['age'] == '':
            self.errors.append("You must enter an age.")
        
        if self.data[n]['email'] == '':
            self.errors.append("You must enter an email.")
        elif '@' not in self.data[n]['email']:
            self.errors.append("Email invalid.")
        
        if self.data[n]['pw'] != self.data[n]['pw2']:
            self.errors.append("Passwords do not match.")
        if len(self.data[n]['pw']) < 4:
            self.errors.append("Password is too short.")

        self.data[n]['pw'] = self.hashPassword(self.data[n]['pw'])
        u=user()
        if u.getByEmail(self.data[n]['email']):
            self.errors.append("Email already exists.")
        
        if len(self.errors)>0:
            return False
        else:
            return True
    def verify_update(self,n=0):
        self.errors = []
        if self.data[n]['fname'] == '':
            self.errors.append("You must enter a first name.")
        if self.data[n]['lname'] == '':
            self.errors.append("You must enter a last name.")
        if len(self.data[n]['pw']) == 0:
            del self.data[n]['pw']
        elif len(self.data[n]['pw']) > 0:
            if self.data[n]['pw'] != self.data[n]['pw2']:
                self.errors.append("Passwords do not match.")
            if len(self.data[n]['pw']) < 4:
                self.errors.append("Password is too short.")
 
            self.data[n]['pw'] = self.hashPassword(self.data[n]['pw'])   
            
        if self.data[n]['email'] == '':
            self.errors.append("You must enter an email.")
        elif '@' not in self.data[n]['email']:
            self.errors.append("Email invalid.")
        
        if len(self.errors)>0:
            return False
        else:
             
            return True
            
    def hashPassword(self,pw):
        m = hashlib.md5()
        m.update(pw)
        return m.hexdigest()
    def getRoleMenu(self):
        r = self.data[0]['role']
        if r == '':
            r = 0
        buf = '<select name="role">'
        for role in self.roleList:
            if str(r) == role[1]:
                sel = 'selected="true"'
            else:
                sel = ''
            buf += '<option '+sel+' value="'+role[1]+'">'+role[0]+'</option>'
        buf += '</select>'
        print buf
        return buf
    def tryLogin(self,un,pw):
        self.data = []
        pw = self.hashPassword(pw)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" WHERE `email` = %s AND `pw` = %s LIMIT 0,1;"
        cur.execute(sql,(un,pw))
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()
    def getDropDown(self):
        buf = '<select name="user_id">'
        for usr in self.data:

            buf += '<option value="'+str(usr['user_id'])+'">'+usr['fname']+ " " +usr['email']+'</option>'
        buf += '</select>'
        print buf
        return buf
    def getByEmail(self,un):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" WHERE `email` = %s LIMIT 0,1;"
        cur.execute(sql,(un))
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()
    def deleteByEmail(self,email):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "DELETE FROM " + self.tn +" WHERE `email` = %s;"
        cur.execute(sql,(email))
        cur.close() 