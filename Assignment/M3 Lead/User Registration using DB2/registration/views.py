from flask import Blueprint, redirect, render_template, request, flash
import ibm_db
import re # regular expression

blue_print = Blueprint("blue_print", "__name__")
conn = ibm_db.connect(
    'DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=lyj74327;PWD=GyaX2qeL2cwuxneg', '', ''
)

@blue_print.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        # getting user data
        email = request.form.get('email')
        password = request.form.get('password')

        # input validation
        if len(email) < 5:
            flash("Email must be atleast 10 characters long", category="error")

        elif len(password) < 6:
            flash("Password must be atleast 6 characters long", category="error")

        else:
            # checking: user already exists or not
            sql_check_query = "SELECT * FROM user WHERE email = ?"
            stmt = ibm_db.prepare(conn, sql_check_query)
            ibm_db.bind_param(stmt, 1, email)
            ibm_db.execute(stmt)

            account = ibm_db.fetch_assoc(stmt)
            print(account)

            if account:
                # email id exists
                # checking if the password is correct
                if not account['PASSWORD'] == password:
                    flash('Invalid password', category='error')

                else:
                    # user entered the correct password
                    # redirecting the user to the dashboard
                    return render_template('dashboard.html', account=account)

            else:
                # email id does not exist in the database
                flash('Email invalid... Try Again', category='error')
            
        return render_template('login.html')

    return render_template('login.html')

@blue_print.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        # getting user data
        username = request.form.get('username')
        email = request.form.get('email')
        number = request.form.get('number')
        password = request.form.get('password')

        # validating user data
        if(len(number) < 5):
            flash("Reg. No must be 5 numbers long", category="error")

        elif not re.match(r'^[a-zA-Z]*$', username):
            flash("Use only alphabets in username", category="error")

        elif len(username) < 4:
            flash("Username must be atleast 6 characters long", category="error")

        elif len(password) < 4:
            flash("Password must be atleast 6 characters long", category="error")

        elif len(email) < 6:
            flash("Email must be atleast 10 characters long", category="error")

        else:
            # checking: user already exists or not
            sql_check_query = "SELECT * FROM user WHERE email = ?"
            stmt = ibm_db.prepare(conn, sql_check_query)
            ibm_db.bind_param(stmt, 1, email)
            ibm_db.execute(stmt) 

            account = ibm_db.fetch_assoc(stmt)

            # email id does not exist in the database
            if not account:
                # inserting the data into the database
                sql_insert_query = "INSERT INTO user VALUES (?, ?, ?, ?)"
                stmt = ibm_db.prepare(conn, sql_insert_query)
                ibm_db.bind_param(stmt, 1, username)
                ibm_db.bind_param(stmt, 2, email)
                ibm_db.bind_param(stmt, 3, int(number))
                ibm_db.bind_param(stmt, 4, password)
                ibm_db.execute(stmt)

                # user data inserted into the database
                # redirecting to login page
                flash('User created successfully! Please Login', category='success')
                return redirect('/')

            else:
                flash('Email id already exists! Try another one', category='error')

        return render_template('register.html')

    return render_template('register.html')

@blue_print.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
