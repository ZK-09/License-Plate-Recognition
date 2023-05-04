# Programmer Name : TAN ZE KAI - TP 061463
# Program Name : main.py
# Description : 
# '''
# This MAIN python file consists of the flask web pages
# It consists of logic and funtion of the webpages
# ''' 
# First Written Date : 4th April 2023
# Last Modified Date : 16th April 2023

from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import session
from flask import flash
from flask_mysqldb import MySQL  
from datetime import timedelta
from Customer import Customer   # Customer class
from Admin import Admin # Admin class

app = Flask(__name__)
mysql = MySQL(app)
app.secret_key = 'w3def5t#frwfe&&*%F'   # Secret Key
app.permanent_session_lifetime = timedelta(minutes=5)
admin_ = Admin(None, None, app, mysql)  # Admin Object
user = Customer(None, None, app, mysql) # Customer Object

# Login Interface ( Customer & Admin )
@app.route("/", methods=['POST','GET'])
def login():
    if request.method == 'POST':
        session.permanent = True    # Session Permanent for 5 Min
        username = request.form['username_input']
        password = request.form['password_input']
        
        # Call Customer Class
        user.username = username
        user.password = password
        results = user.login()
        
        # Call Admin Class
        admin_.username = username
        admin_.password = password
        admin_results = admin_.login()
        
        if results:
            session['loggedin'] = True
            session['username'] = results[0]    # Session 
            return redirect(url_for('balance'))
        elif admin_results:
            return redirect(url_for('admin'))
        else:
            flash('Username/Password is incorrect', 'alert alert-danger')
            return redirect(url_for('login'))
    else:
        if 'username' in session:
            return redirect(url_for('balance'))
        else:
            return render_template("login.html")

# Redirect to Forget Password Interface
@app.route("/forgetPassword")
def forget_password():    
    return render_template("forget_password.html")

# Confirm Phone Num Interface
@app.route("/phoneConfirm", methods=['POST','GET'])
def confirm_phone_num():
    if request.method == 'GET':
        return render_template("forget_password.html")

    if request.method == 'POST':
        phone_num = request.form['_phone_num']
        results = user.confirm_phone_num(phone_num)
        
        if results :           
            session['phone_num'] = user.phone_num
            return redirect(url_for('reset_password'))
        else:
            flash('This User does not exist !')
            return redirect(url_for('forget_password'))
        
# Reset Password Interface
@app.route("/resetPassword", methods=['POST','GET'])
def reset_password():
    if request.method == 'GET':
        return render_template("reset_password.html")
    
    if request.method == 'POST':
        new_pass = request.form['new_pass']
        re_new_pass = request.form['re_new_pass']
        _valid, _msg = user.reset_password(new_pass, re_new_pass)  # Method Call
        print(_valid, _msg)
        if _valid is True:            
            flash(_msg, 'alert alert-success')
            return redirect(url_for('login'))        
        else:
            flash(_msg, 'alert alert-danger')
            return render_template("reset_password.html")

# Customer view their balance amount
@app.route("/balanceAmount")
def balance():  
    if 'username' in session:
        username = session['username']
        balance_ = user.check_balance(username) 
        if balance_ is None:
            balance_ = 0
        return render_template("balance_check.html", balance=balance_)
    else:
        return redirect(url_for('login'))

# Top Up Customer Amount
@app.route("/topUpAmount", methods=['POST','GET'])
def reload_balance():
    if request.method == 'GET':
        return render_template("balance_check.html")
    
    if request.method == 'POST':
        amount = request.form['topup_amount']
        print(type(amount))
        user.top_up_balance(amount)   # Top UP Method
        
        return redirect(url_for('balance'))

# Customer Record ( View By Customer Only )
@app.route("/customerRecord")
def customer_record():
    record_list = user.view_record()
    return render_template("customer_record.html", record_list = record_list)

## Admin 
@app.route("/adminLogin")
def admin():
    return render_template("admin_register.html")

# Admin register new vehicle Interface
@app.route("/register", methods=['POST','GET'])
def admin_register():
    if request.method == 'GET':
        return render_template('admin_register.html')
    
    if request.method == 'POST':
        _username = request.form['inputUsername']
        _password = request.form['inputPassword']
        _gender = request.form['inputGender']
        _phone = request.form['inputPhone']
        _vehicle = request.form['inputVehicle']
        _model = request.form['inputModel']
        
        _flag, _msg = admin_.register_vehicle(_username, _password, _gender, _phone, _vehicle, _model)
        if _flag is True:
            flash(f'Vehicle {_vehicle} has registered successfully', 'alert alert-success')
            return redirect(url_for('admin_register'))
        else:
            flash(_msg, 'alert alert-danger')
            return redirect(url_for('admin_register'))

# Admin view record Interface
@app.route("/record", methods=['POST','GET'])
def admin_record():
    if request.method == 'GET':
        record_list = admin_.view_history()
        return render_template('admin_record.html', record_list = record_list)
    
    input_search = request.form['inputSearch'].upper()
    if request.method == 'POST':
        record_list = admin_.search_history(input_search)
        
        return render_template('admin_record.html', record_list = record_list)
    
    return render_template('admin_record.html', record_list = record_list)

# Add Vehicle from the same user
@app.route("/newVehicle", methods=['POST','GET'])
def admin_add_vehicle():
    if request.method == 'GET':
        return render_template('admin_add_vehicle.html')
    
    if request.method == 'POST':
        _username = request.form['inputUsername']
        _vehicle = request.form['inputVehicle']
        _model = request.form['inputModel']
        
        _flag = admin_.vehicle_number(_vehicle)
        if _flag is True:
            admin_.add_vehicle(_username, _vehicle, _model)
            flash(f'Vehicle {_vehicle} has registered successfully', 'alert alert-success')
            return redirect(url_for('admin_add_vehicle'))
        else:
            flash(f'Vehicle {_vehicle} has duplicated record', 'alert alert-danger')
            return redirect(url_for('admin_add_vehicle'))
# Logout
@app.route("/Logout")
def logout():
    session.pop('username', None)
    session.pop('loggedin', False)
    return redirect(url_for('login'))
    
if __name__ == "__main__":
    app.run(debug=True)