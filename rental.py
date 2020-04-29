from baseObject import baseObject
from vehicle import vehicle
import pymysql
class rental(baseObject):
    def __init__(self):
        tn = 'collins_rental2'
        pk = 'rental_id'
        user_id = 'user_id'
        self.setupObject(tn,pk)

    def verify_rental(self,n=0):
        self.errors = []
        print self.data
        if self.data[n]['rental_startdate'] == '':
            self.errors.append("You must enter the start date of the rental.")
        if self.data[n]['rental_duration'] == '':
            self.errors.append("You must enter the end date of the rental.")
        if self.data[n]['rental_duration'] < 1:
            self.errors.append("You must a positive number of days")
        else:
            v = vehicle()
            v.getById(self.data[n]['vehicle_id'])
            self.data[n]['rental_price'] = int(self.data[n]['rental_duration']) * int(v.data[0]['price_per_day'])
            print self.data[n]['rental_price']
        if self.data[n]['rental_price'] == '':
            self.errors.append("You must enter the price of the rental.")
        if self.data[n]['rental_insurance'] == '':
            self.errors.append("You must enter the insurance of the vehicle.")
        if self.data[n]['vehicle_id'] == '':
            self.errors.append("You must enter the ID of the vehicle.")
        if len(self.errors)>0:
            return False
        else:
            return True

    def getCustomerRentals(self,user_id):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" left join `collins_vehicle2` on `collins_vehicle2`.vehicle_id = `collins_rental2`.vehicle_id WHERE `user_id` = %s;"
        cur.execute(sql,(user_id))
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()

    def getAll(self):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" left join `collins_vehicle2` on `collins_vehicle2`.vehicle_id = `collins_rental2`.vehicle_id;"
        cur.execute(sql)
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()
