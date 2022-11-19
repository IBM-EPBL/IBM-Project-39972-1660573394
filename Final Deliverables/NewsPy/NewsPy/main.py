from flask import Flask, render_template, request, redirect, url_for, session,flash
import requests 
from flask_mysqldb import MySQL
import ibm_db
import random
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e'

# Enter your database connection details below

conn = ibm_db.connect(
    'DATABASE=bludb;'
    'HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;'
    'PORT=32716;'
    'SECURITY=SSL;'
    'UID=rcv18228;'
    'PWD=PSEaguZ3EINJmR9F;', '', ''
)

@app.route('/test')
def test():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST':
        # getting user data
        email = request.form.get('username')
        password = request.form.get('password')
        sql_check_query = "SELECT * FROM user WHERE username = ?"
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
                session['USERNAME'] = account['USERNAME']
                session['loggedin'] = True
                return redirect('/home')

        else:
            # email id does not exist in the database
            flash('Email invalid... Try Again', category='error')
            
        return render_template('auth/login.html')
    
    return render_template('auth/login.html')



# http://localhost:5000/pythinlogin/register 
# This will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST':
        # getting user data
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        # checking: user already exists or not
        sql_check_query = "SELECT * FROM user WHERE email = ?"
        stmt = ibm_db.prepare(conn, sql_check_query)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt) 

        account = ibm_db.fetch_assoc(stmt)
        # email id does not exist in the database
        if not account:
            # inserting the data into the database
            sql_insert_query = "INSERT INTO user VALUES (?, ?, ?)"
            stmt = ibm_db.prepare(conn, sql_insert_query)
            ibm_db.bind_param(stmt, 1, email)
            ibm_db.bind_param(stmt, 2, password)
            ibm_db.bind_param(stmt, 3, username)
            ibm_db.execute(stmt)

            # user data inserted into the database
            # redirecting to login page
            flash('User created successfully! Please Login', category='success')
            return redirect('/')

        else:
            flash('Email id already exists! Try another one', category='error')

        return render_template('auth/register.html')

    return render_template('auth/register.html')

@app.route('/home', methods=['GET'])
def home():

    categories = ['Magazines', 'Books', 'Movies', 'Music', 'Games', 'Electronics', 'Computers']
    
    NewsCategory = ['Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology', 'World','International','Tech','It','Software' ]
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        searchQuery = request.args.get('query') 
        # //searchQuery is empty default value is bitcoin 
        # random NewsCategory = random.choice(NewsCategory)
        if searchQuery is None:
            searchQuery = random.choice(NewsCategory)
        
        API_KEY = 'bedc8423bb4944a995b9533870f64e62'
        BASE_URL = 'https://newsapi.org/v2/'
        # get data from api https://newsapi.org/v2/everything?q=searchQuery&apiKey=API_KEY
        url = BASE_URL + 'everything?q=' + searchQuery + '&apiKey=' + API_KEY
        response = requests.get(url)
        data = response.json()

        first_article = data['articles'][0]
        three_articles = data['articles'][1:4]
                  
        return render_template('index.html',categories=categories, NewsCategory=NewsCategory ,username=session['USERNAME'],title="Homes", data=data, first_article=first_article, three_articles=three_articles)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))    


@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('auth/profile.html', username=session['USERNAME'],title="Profile")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))  



if __name__ =='__main__':
    app.run(debug=True)
