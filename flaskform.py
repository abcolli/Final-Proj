from baseObject import baseObject
from user import user
from vehicle import vehicle
from rental import rental
from inspection import inspection
from rental import rental
import time


from flask import Flask
from flask import request,session, redirect, url_for, escape,send_from_directory

import pymysql 
import json

app = Flask(__name__, static_url_path='')


SESSION_TIME = 1000
global SESSION_TIME 

def record(msg):
    print msg

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


    
@app.route("/test", methods=['GET','POST'])
def test():
    if session.get('login_time') is not None:
        print "TEST"
        if time.time() - session.get('login_time') < SESSION_TIME:
            return "login ok " + str(time.time() - session.get('login_time')) + str(session['user_data'])
    return "not logged in"
@app.route("/data", methods=['GET','POST'])
def data():
    return '''
    <form action="/data" method="POST">
            Enter string<br>
            <input type="text" name="email"/>
            <br><br>
            
            <input type="submit" value="Submit"/>
        </form>'''
    
@app.route("/", methods=['GET','POST'])
def login():
    print request.args.get('action')
    msg = "Login"
    if request.args.get('action') == 'login':
        u = user()
        if u.tryLogin(request.form.get('email'),request.form.get('password')):
            session['login_time'] = time.time()
            session['user_data'] = u.data[0]
            return header() + "Login Successful <br> Welcome " + str(u.data[0]['fname']) + mainMenu() + footer()
        else:
            msg = "Login failed"
    elif request.args.get('action') == 'logout':
        session['login_time'] = None
        session['user_data'] = None
        msg = 'Logout successful.'
        
    return header() + msg + '''
    
    <div >
        <form action="/?action=login" method="POST">
            Email:<br>
            <input type="text" name="email"/>
            <br><br>
            Password:<br>
            <input type="password" name="password"/>
            <br><br>
            <input type="submit" value="Login"/>
        </form>
    </div>
    '''  + footer() 
@app.route('/user/<user_id>',methods=['GET','POST'])
def edit_user(user_id):
    emsg = ''
    if not checkSession(2):
        return redirect("/mainmenu")
    u = user()
    if request.args.get('action') == 'update':
        u.getById(user_id)
        u.data[0]['fname'] = request.form.get('fname')
        u.data[0]['lname'] = request.form.get('lname')
        u.data[0]['email'] = request.form.get('email')
        u.data[0]['age'] = request.form.get('age')
        u.data[0]['role'] = request.form.get('role')
        u.data[0]['pw'] = request.form.get('pw')
        u.data[0]['pw2'] = request.form.get('pw2')
        if u.verify_update():
            u.update()
            emsg = 'User updated.'
        else:
            emsg = '<div style="color:red;">'+u.getErrorHTML()+'</div>'
    if request.args.get('action') == 'insert':
        u.createBlank()
        print u.data
        u.data[0]['fname'] = request.form.get('fname')
        u.data[0]['lname'] = request.form.get('lname')
        u.data[0]['email'] = request.form.get('email')
        u.data[0]['age'] = request.form.get('age')
        u.data[0]['role'] = request.form.get('role')
        u.data[0]['pw'] = request.form.get('pw')
        u.data[0]['pw2'] = request.form.get('pw2')
        print u.data
        if u.verify_new():
            u.insert()
            emsg = 'User added.'
        else:
            emsg = '<div style="color:red;">'+u.getErrorHTML()+'</div>'      
            
    if user_id == 'new':
        u.createBlank()
        w = 'Add'
        a = 'insert'
    else:   
        u.getById(user_id)
        w = 'Edit'
        a = 'update'
    html ='''
    <b>'''+w+''' User '''+user_id+'''</b><br><br>
    '''+emsg+'''
    <form action="/user/'''+str(user_id)+'''?action='''+a+'''" method="POST">
        Email<br>
        <input name="email" type="text" value="'''+u.data[0]['email']+'''" /><br>
        Password (leave blank for no change)<br>
        <input name="pw" type="text" value="" /><br>
        Retype Password<br>
        <input name="pw2" type="text" value="" /><br>
        First name<br>
        <input name="fname" type="text" value="'''+u.data[0]['fname']+'''" /><br>
        Last name<br>
        <input name="lname" type="text" value="'''+u.data[0]['lname']+'''" /><br>
        Age<br>
        <input name="age" type="text" value="'''+u.data[0]['age']+'''" /><br>
        Role<br>
        '''+u.getRoleMenu()+'''
        
        <br><br>
        <input type="submit" value="Submit"/><br>
        <a href="/mainmenu">Main Menu</a><br>
    </form>
    
    '''
    
    return header()+html+footer()

@app.route('/vehicle/<vehicle_id>',methods=['GET','POST'])
def edit_vehicle(vehicle_id):
    emsg = ''
    if not checkSession(2):
        return redirect("/mainmenu")
    v = vehicle()
    if request.args.get('action') == 'update':
        v.getById(vehicle_id)
        v.data[0]['make'] = request.form.get('make')
        v.data[0]['model'] = request.form.get('model')
        v.data[0]['year'] = request.form.get('year')
        v.data[0]['vehicle_type'] = request.form.get('vehicle_type')
        v.data[0]['color'] = request.form.get('color')
        v.data[0]['price_per_day'] = request.form.get('price_per_day')
        v.data[0]['vin_number'] = request.form.get('vin_number')
        v.data[0]['rental_status'] = request.form.get('rental_status')
        if v.verify_vehicle():
            v.update()
            emsg = 'Vehicle updated.'
        else:
            emsg = '<div style="color:red;">'+v.getErrorHTML()+'</div>'
    if request.args.get('action') == 'insert':
        v.createBlank()
        print v.data
        v.data[0]['make'] = request.form.get('make')
        v.data[0]['model'] = request.form.get('model')
        v.data[0]['year'] = request.form.get('year')
        v.data[0]['vehicle_type'] = request.form.get('vehicle_type')
        v.data[0]['color'] = request.form.get('color')
        v.data[0]['price_per_day'] = request.form.get('price_per_day')
        v.data[0]['vin_number'] = request.form.get('vin_number')
        v.data[0]['rental_status'] = request.form.get('rental_status')
        print v.data
        if v.verify_vehicle():
            v.insert()
            emsg = 'Vehicle added.'
        else:
            emsg = '<div style="color:red;">'+v.getErrorHTML()+'</div>'      
            
    if vehicle_id == 'new':
        v.createBlank()
        w = 'Add'
        a = 'insert'
    else:   
        v.getById(vehicle_id)
        w = 'Edit'
        a = 'update'
    html ='''
    <b>'''+w+''' Vehicle '''+vehicle_id+'''</b><br><br>
    '''+emsg+'''
    <form action="/vehicle/'''+str(vehicle_id)+'''?action='''+a+'''" method="POST">
        Make<br>
        <input name="make" type="text" value="'''+v.data[0]['make']+'''" /><br>
        Model<br>
        <input name="model" type="text" value="'''+v.data[0]['model']+'''" /><br>
        Year<br>
        <input name="year" type="text" value="'''+v.data[0]['year']+'''" /><br>
        Vehicle Type<br>
        <input name="vehicle_type" type="text" value="'''+v.data[0]['vehicle_type']+'''" /><br>
        Color<br>
        <input name="color" type="text" value="'''+v.data[0]['color']+'''" /><br>
        Price per Day<br>
        <input name="price_per_day" type="text" value="'''+v.data[0]['price_per_day']+'''" /><br>
        Vin Number<br>
        <input name="vin_number" type="text" value="'''+v.data[0]['vin_number']+'''" /><br>
        Rental Status<br>
        '''+v.getRentalStatus()+'''<br>
        <br><br>
        <input type="submit" value="Submit"/><br>
        <a href="/mainmenu">Main Menu</a><br>
    </form>
    
    '''
    
    return header()+html+footer()

@app.route('/inspection/<inspection_id>',methods=['GET','POST'])
def edit_inspection(inspection_id):
    emsg = ''
    if not checkSession(2):
        return redirect("/mainmenu")
    s = inspection()
    if request.args.get('action') == 'update':
        s.getById(inspection_id)
        s.data[0]['inspection_date'] = request.form.get('inspection_date')
        s.data[0]['inspection_type'] = request.form.get('inspection_type')
        s.data[0]['damages'] = request.form.get('damages')
        s.data[0]['damage_value'] = request.form.get('damage_value')
        s.data[0]['vehicle_id'] = request.form.get('vehicle_id')
        s.data[0]['employee_id'] = request.form.get('employee_id')
        if s.verify_inspection():
            s.update()
            emsg = 'Inspection updated.'
        else:
            emsg = '<div style="color:red;">'+s.getErrorHTML()+'</div>'
    if request.args.get('action') == 'insert':
        s.createBlank()
        print s.data
        s.data[0]['inspection_date'] = request.form.get('inspection_date')
        s.data[0]['inspection_type'] = request.form.get('inspection_type')
        s.data[0]['damages'] = request.form.get('damages')
        s.data[0]['damage_value'] = request.form.get('damage_value')
        s.data[0]['vehicle_id'] = request.form.get('vehicle_id')
        s.data[0]['employee_id'] = request.form.get('employee_id')
        if s.verify_inspection():
            s.insert()
            emsg = 'Inspection added.'
        else:
            emsg = '<div style="color:red;">'+s.getErrorHTML()+'</div>'      
            
    if inspection_id == 'new':
        s.createBlank()
        w = 'Add'
        a = 'insert'
    else:   
        s.getById(inspection_id)
        w = 'Edit'
        a = 'update'
    html ='''
    <b>'''+w+''' Inspection '''+inspection_id+'''</b><br><br>
    '''+emsg+'''
    <form action="/inspection/'''+str(inspection_id)+'''?action='''+a+'''" method="POST">
        Inspection Date<br>
        <input name="inspection_date" type="date" value="'''+s.data[0]['inspection_date']+'''" /><br>
        Inspection Type<br>
        '''+s.getinspectionMenu()+'''<br>
        Damages<br>
        <input name="damages" type="text" value="'''+s.data[0]['damages']+'''" /><br>
        Damage Value<br>
        <input name="damage_value" type="text" value="'''+s.data[0]['damage_value']+'''" /><br>
        Vehicle ID<br>
        <input name="vehicle_id" type="text" value="'''+s.data[0]['vehicle_id']+'''" /><br>
        Employee ID<br>
        <input name="employee_id" type="text" value="'''+s.data[0]['employee_id']+'''" /><br>
        <br><br>
        <input type="submit" value="Submit"/><br>
        <a href="/mainmenu">Main Menu</a><br>
    </form>
    
    '''
    
    return header()+html+footer()

@app.route('/rental/<rental_id>',methods=['GET','POST'])
def edit_rentalcustomer(rental_id):
    emsg = ''
    if not checkSession(1):
        return redirect("/mainmenu")
    r = rental()
    v = vehicle()
    v.getAvailableVehicles()
    if request.args.get('action') == 'insert':
        r.createBlank()
        print r.data
        r.data[0]['rental_startdate'] = request.form.get('rental_startdate')
        r.data[0]['rental_duration'] = request.form.get('rental_duration')
        r.data[0]['rental_price'] = request.form.get('rental_price')
        r.data[0]['rental_insurance'] = request.form.get('rental_insurance')
        r.data[0]['user_id'] = session['user_data']['user_id']
        r.data[0]['vehicle_id'] = request.form.get('vehicle_id')
        if r.verify_rental():
            r.insert()
            emsg = 'Rental added.'
        else:
            emsg = '<div style="color:red;">'+r.getErrorHTML()+'</div>'      
            
    if rental_id == 'new':
        r.createBlank()
        w = 'Add'
        a = 'insert'
    else:   
        r.getById(rental_id)
        w = 'Edit'
        a = 'update'
    html ='''
    <b>'''+w+''' Rental '''+rental_id+'''</b><br><br>
    '''+emsg+'''
    <form action="/rental/'''+str(rental_id)+'''?action='''+a+'''" method="POST">
        Rental Start Date<br>
        <input name="rental_startdate" type="date" value="'''+r.data[0]['rental_startdate']+'''" /><br>
        Rental Duration<br>
        <input name="rental_duration" type="number" value="'''+r.data[0]['rental_duration']+'''" /><br>
        Vehicle<br>
        '''+v.getAvailableDropDown()+'''<br>
        Rental Price<br>
        <input name="rental_price" type="text" value="'''+str(r.data[0]['rental_price'])+'''" /><br>
        Rental Insurance<br>
        <input name="rental_insurance" type="text" value="'''+r.data[0]['rental_insurance']+'''" /><br>
        <br><br>
        <input type="submit" value="Submit"/><br>
        <a href="/mainmenu">Main Menu</a><br>
    </form>
    
    '''
    
    return header()+html+footer()

@app.route('/rentalemp/<rental_id>',methods=['GET','POST'])
def edit_rentalemployee(rental_id):
    emsg = ''
    if not checkSession(2):
        return redirect("/mainmenu")
    r = rental()
    v = vehicle()
    v.getAvailableVehicles()
    if request.args.get('action') == 'insert':
        r.createBlank()
        print r.data
        r.data[0]['rental_startdate'] = request.form.get('rental_startdate')
        r.data[0]['rental_duration'] = request.form.get('rental_duration')
        r.data[0]['rental_price'] = request.form.get('rental_price')
        r.data[0]['rental_insurance'] = request.form.get('rental_insurance')
        r.data[0]['user_id'] = session['user_data']['user_id']
        r.data[0]['vehicle_id'] = request.form.get('vehicle_id')
        if r.verify_rental():
            r.insert()
            emsg = 'Rental added.'
        else:
            emsg = '<div style="color:red;">'+r.getErrorHTML()+'</div>'      
            
    if rental_id == 'new':
        r.createBlank()
        w = 'Add'
        a = 'insert'
    else:   
        r.getById(rental_id)
        w = 'Edit'
        a = 'update'
    au = user()
    au.getAll()
    html ='''
    <b>'''+w+''' Rental '''+rental_id+'''</b><br><br>
    '''+emsg+'''
    <form action="/rental/'''+str(rental_id)+'''?action='''+a+'''" method="POST">
        Rental Start Date<br>
        <input name="rental_startdate" type="date" value="'''+r.data[0]['rental_startdate']+'''" /><br>
        Rental Duration<br>
        <input name="rental_duration" type="number" value="'''+r.data[0]['rental_duration']+'''" /><br>
        Vehicle<br>
        '''+v.getAvailableDropDown()+'''<br>
        Customer<br>
        '''+au.getDropDown()+'''<br>
        Rental Price<br>
        <input name="rental_price" type="text" value="'''+str(r.data[0]['rental_price'])+'''" /><br>
        Rental Insurance<br>
        <input name="rental_insurance" type="text" value="'''+r.data[0]['rental_insurance']+'''" /><br>
        <br><br>
        <input type="submit" value="Submit"/><br>
        <a href="/mainmenu">Main Menu</a><br>
    </form>
    
    '''
    
    return header()+html+footer()

    
@app.route("/users", methods=['GET','POST'])
def list_users():
    if not checkSession(2):
        return redirect("/mainmenu")
    html = ''' <b> Users </b>
    <table style="width:600px;">
        <tr style="background-color:#bbb;">
            <td>User_ID</td>
            <td>Name</td>
            <td>Email</td>
            <td>Role</td>
        </tr>'''
    u = user()
    u.getAll()
    i = 0
    for row in u.data:
        c = '#eee;'
        if i % 2 == 0:
            c ='#ddd;'
        html +='''<tr style="background-color:'''+c+''''">
            <td> <a href="/user/'''+str(row['user_id'])+'''">'''+str(row['user_id'])+'''</a> </td>
            <td>'''+str(row['fname'])+'''</td>
            <td>'''+str(row['email'])+'''</td>
            <td>'''+str(row['role'])+'''</td>
        </tr>'''
        i+=1
    
    html += '''</table>
    <a href="user/new">Create New User</a><br><br>
    <a href="/mainmenu">Main Menu</a><br>'''
    return header() + html + footer()

@app.route("/vehicle", methods=['GET','POST'])
def list_vehicle():
    if not checkSession(2):
        return redirect("/mainmenu")
    html = ''' <b> Vehicles </b>
    <table style="width:600px;">
        <tr style="background-color:#bbb;">
            <td>Vehicle ID</td>
            <td>Make</td>
            <td>Model</td>
            <td>Year</td>
            <td>Vehicle Type</td>
            <td>Color</td>
            <td>Price per Day</td>
            <td>Vin Number</td>
            <td>Rental Status</td>
        </tr>'''
    v = vehicle()
    v.getAll()
    i = 0
    for row in v.data:
        c = '#eee;'
        if i % 2 == 0:
            c ='#ddd;'
        html +='''<tr style="background-color:'''+c+''''">
            <td> <a href="/vehicle/'''+str(row['vehicle_id'])+'''">'''+str(row['vehicle_id'])+'''</a> </td>
            <td>'''+str(row['make'])+'''</td>
            <td>'''+str(row['model'])+'''</td>
            <td>'''+str(row['year'])+'''</td>
            <td>'''+str(row['vehicle_type'])+'''</td>
            <td>'''+str(row['color'])+'''</td>
            <td>'''+str(row['price_per_day'])+'''</td>
            <td>'''+str(row['vin_number'])+'''</td>
            <td>'''+str(row['rental_status'])+'''</td>
        </tr>'''
        i+=1
    
    html += '''</table>
    <a href="vehicle/new">Add New Vehicle</a><br>
    <br><a href = "/mainmenu">Main Menu</a><br>
    '''
    return header() + html + footer()
@app.route("/inspection", methods=['GET','POST'])
def list_inspection():
    if not checkSession(2):
        return redirect("/mainmenu")
    html = ''' <b> Inspections </b>
    <table style="width:600px;">
        <tr style="background-color:#bbb;">
            <td>Inspection ID</td>
            <td>Date</td>
            <td>Inspection Type</td>
            <td>Damages</td>
            <td>Damage Value</td>
            <td>Vehicle ID</td>
            <td>Employee ID</td>
        </tr>'''
    s = inspection()
    s.getAll()
    i = 0
    for row in s.data:
        c = '#eee;'
        if i % 2 == 0:
            c ='#ddd;'
        html +='''<tr style="background-color:'''+c+''''">
            <td> <a href="/inspection/'''+str(row['inspection_id'])+'''">'''+str(row['inspection_id'])+'''</a> </td>
            <td>'''+str(row['inspection_date'])+'''</td>
            <td>'''+str(row['inspection_type'])+'''</td>
            <td>'''+str(row['damages'])+'''</td>
            <td>'''+str(row['damage_value'])+'''</td>
            <td>'''+str(row['vehicle_id'])+'''</td>
            <td>'''+str(row['employee_id'])+'''</td>
        </tr>'''
        i+=1
    
    html += '''</table>
    <a href="inspection/new">Add New Inspection</a><br>
    <br><a href = "/mainmenu">Main Menu</a><br>
    '''
    return header() + html + footer()

@app.route("/rentalemp", methods=['GET','POST'])
def list_rental():
    if not checkSession(2):
        return redirect("/mainmenu")
    html = ''' <b> Rentals </b>
    <table style="width:600px;">
        <tr style="background-color:#bbb;">
            <td>Rental ID</td>
            <td>Start Date</td>
            <td>Return Date</td>
            <td>Rental Price</td>
            <td>Rental Insurance</td>
            <td>Make</td>
            <td>Model</td>
        </tr>'''
    r = rental()
    r.getAll()
    i = 0
    for row in r.data:
        c = '#eee;'
        if i % 2 == 0:
            c ='#ddd;'
        html +='''<tr style="background-color:'''+c+''''">
            <td> <a href="/rental/'''+str(row['rental_id'])+'''">'''+str(row['rental_id'])+'''</a> </td>
            <td>'''+str(row['rental_startdate'])+'''</td>
            <td>'''+str(row['rental_duration'])+'''</td>
            <td>'''+str(row['rental_price'])+'''</td>
            <td>'''+str(row['rental_insurance'])+'''</td>
            <td>'''+str(row['make'])+'''</td>
            <td>'''+str(row['model'])+'''</td>
        </tr>'''
        i+=1
    
    html += '''</table>
    <a href="rentalemp/new">Add New Rental</a><br>
    <br><a href = "/mainmenu">Main Menu</a><br>
    '''
    return header() + html + footer()

@app.route("/customerrentals", methods=['GET','POST'])
def list_customerrental():
    if not checkSession(1):
        return redirect("/mainmenu")
    html = ''' <b> Customer Rentals</b>
    <table style="width:600px;">
        <tr style="background-color:#bbb;">
            <td>User ID</td>
            <td>Rental ID</td>
            <td>Start Date</td>
            <td>Duration</td>
            <td>Rental Price</td>
            <td>Rental Insurance</td>
            <td>Make</td>
            <td>Model</td>
        </tr>'''
    r = rental()
    r.getCustomerRentals(session['user_data']['user_id'])
    i = 0
    for row in r.data:
        c = '#eee;'
        if i % 2 == 0:
            c ='#ddd;'
        html +='''<tr style="background-color:'''+c+''''">
            <td>'''+str(row['user_id'])+'''</td>
            <td>'''+str(row['rental_id'])+'''</td>
            <td>'''+str(row['rental_startdate'])+'''</td>
            <td>'''+str(row['rental_duration'])+'''</td>
            <td>'''+str(row['rental_price'])+'''</td>
            <td>'''+str(row['rental_insurance'])+'''</td>
            <td>'''+str(row['make'])+'''</td>
            <td>'''+str(row['modelr'])+'''</td>
        </tr>'''
        i+=1
    
    html += '''</table>
    <a href="rental/new">Add New Rental</a>
    <br><a href = "/mainmenu">Main Menu</a><br>
    '''
    return header() + html + footer()

@app.route("/availablevehicles", methods=['GET','POST'])
def list_availablevehicles():
    if not checkSession(1):
        return redirect("/mainmenu")
    html = ''' <b> Available Vehicles </b>
    <table style="width:600px;">
        <tr style="background-color:#bbb;">
            <td>Vehicle ID</td>
            <td>Make</td>
            <td>Model</td>
            <td>Year</td>
            <td>Vehicle Type</td>
            <td>Color</td>
            <td>Price per Day</td>
            <td>Vin Number</td>
            <td>Rental Status</td>
        </tr>'''
    v = vehicle()
    v.getAvailableVehicles()
    i = 0
    for row in v.data:
        c = '#eee;'
        if i % 2 == 0:
            c ='#ddd;'
        html +='''<tr style="background-color:'''+c+''''">
            <td>'''+str(row['vehicle_id'])+'''</td>
            <td>'''+str(row['make'])+'''</td>
            <td>'''+str(row['model'])+'''</td>
            <td>'''+str(row['year'])+'''</td>
            <td>'''+str(row['vehicle_type'])+'''</td>
            <td>'''+str(row['color'])+'''</td>
            <td>'''+str(row['price_per_day'])+'''</td>
            <td>'''+str(row['vin_number'])+'''</td>
            <td>'''+str(row['rental_status'])+'''</td>
        </tr>'''
        i+=1
    
    html += '''</table>
    <br><a href = "/mainmenu">Main Menu</a><br>
    '''
    return header() + html + footer()



def header():
    return '''<!--Start header-->
    <html>
    <head>
        <title>My Page</title>
        <link rel="stylesheet" href="../static/style.css">
        <link href="https://fonts.googleapis.com/css?family=Mina" rel="stylesheet">
    </head>
    <body class="otherfont">
    <!--End header-->
    '''
def footer():
    return '''
    <!--Start footer-->
    </body>
    <div id="footer">
    
    </div>
    </html>
    <!--End footer-->
    '''
@app.route("/mainmenu", methods=["GET", "POST"])
def mainMenu():
    if checkSession(2):
        return '''
        <div id="mainmenu">
            <br><b>Main Menu</b><br><br>
            <a href="/users">Users</a><br>
            <a href="/vehicle">Vehicles</a><br>
            <a href="/inspection">Inspections</a><br>
            <a href="/rentalemp">Rentals</a><br><br>
            <a href="/?action=logout">Logout</a>

        </div>
        
        '''
    elif checkSession(1):
        return '''
        <div id="mainmenu">
            <br><b>Main Menu</b><br><br>
            <a href="/availablevehicles">Available Vehicles</a><br>
            <a href="/rental/new">Create a Rental</a><br>
            <a href="/customerrentals">Past Customer Rentals</a><br><br>
            <a href="/?action=logout">Logout</a>

        </div>
        
        '''
    else:
        return redirect("/")

def checkSession(n):
    
    if session.get('login_time') is not None:
        if time.time() - session.get('login_time') < SESSION_TIME and str(session['user_data']['role']) >= str(n):
            return True
    return False
    
    
if __name__ == "__main__":
    app.secret_key = 'AdFGsdfgsdfgst545454^Y$^y54'
    app.run(debug=True)

