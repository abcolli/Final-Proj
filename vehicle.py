from baseObject import baseObject
import pymysql
class vehicle(baseObject):
    def __init__(self):
        tn = 'collins_vehicle2'
        pk = 'vehicle_id'
        self.rental_status = [['Not Rented','1'],['Rented','2']]      
        self.setupObject(tn,pk)

    def verify_vehicle(self,n=0):
        self.errors = []
        print self.data
        if self.data[n]['make'] == '':
            self.errors.append("You must enter the make of the vehicle.")
        if self.data[n]['model'] == '':
            self.errors.append("You must enter the model of the vehicle.")
        if self.data[n]['year'] == '':
            self.errors.append("You must enter the year of the vehicle.")
        if len(self.data[n]['year']) != 4:
            self.errors.append("The year must be valid a 4 digits.")
        if self.data[n]['vehicle_type'] == '':
            self.errors.append("You must enter the type of the vehicle.")
        if self.data[n]['color'] == '':
            self.errors.append("You must enter the color of the vehicle.")
        if self.data[n]['price_per_day'] == '':
            self.errors.append("You must enter the price of the vehicle.")
        if self.data[n]['vin_number'] == '':
            self.errors.append("You must enter the vin number of the vehicle.")
        if len(self.errors)>0:
            return False
        else:
            return True

    def getRentalStatus(self):
        r = self.data[0]['rental_status']
        if r == '':
            r = 0
        buf = '<select name="rental_status">'
        for rental in self.rental_status:
            if str(r) == rental[1]:
                sel = 'selected="true"'
            else:
                sel = ''
            buf += '<option '+sel+' value="'+rental[1]+'">'+rental[0]+'</option>'
        buf += '</select>'
        print buf
        return buf

    def getAvailableVehicles(self):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +'''
LEFT JOIN  `collins_inspection2` ON  `collins_inspection2`.vehicle_id =  `collins_vehicle2`.vehicle_id
WHERE  `collins_inspection2`.inspection_type =2
OR  `collins_inspection2`.inspection_type IS NULL 
GROUP BY  `collins_vehicle2`.vehicle_id
ORDER BY  `collins_inspection2`.inspection_id
'''
        cur.execute(sql)
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()

    def getAvailableDropDown(self):
        buf = '<select name="vehicle_id">'
        for car in self.data:

            buf += '<option value="'+str(car['vehicle_id'])+'">'+car['make']+ " " +car['model']+'</option>'
        buf += '</select>'
        print buf
        return buf