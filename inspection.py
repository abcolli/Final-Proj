from baseObject import baseObject
import pymysql
class inspection(baseObject):
    def __init__(self):
        tn = 'collins_inspection2'
        pk = 'inspection_id'
        self.inspectionList = [['Pre-Inspection','1'],['Post-Inspection','2']]
        self.setupObject(tn,pk)
    def verify_inspection(self,n=0):
        self.errors = []
        print self.data
        if self.data[n]['inspection_date'] == '':
            self.errors.append("You must enter the date of the inspection.")
        if self.data[n]['inspection_type'] == '':
            self.errors.append("You must enter the type of the inspection.")
        if self.data[n]['damages'] == '':
            self.errors.append("You must enter the damages of the vehicle.")
        if self.data[n]['damage_value'] == '':
            self.errors.append("You must enter the value of damage to the vehicle.")
        if self.data[n]['vehicle_id'] == '':
            self.errors.append("You must enter the ID of the vehicle.")
        if self.data[n]['employee_id'] == '':
            self.errors.append("You must enter the ID of the employee who performed the inspection.")
        if len(self.errors)>0:
            return False
        else:
            return True

    def getinspectionMenu(self):
        r = self.data[0]['inspection_type']
        if r == '':
            r = 0
        buf = '<select name="inspection_type">'
        for role in self.inspectionList:
            if str(r) == role[1]:
                sel = 'selected="true"'
            else:
                sel = ''
            buf += '<option '+sel+' value="'+role[1]+'">'+role[0]+'</option>'
        buf += '</select>'
        print buf
        return buf
 