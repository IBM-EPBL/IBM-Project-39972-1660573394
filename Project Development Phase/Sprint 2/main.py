from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import random
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e'

# Enter your database connection details below
app.config['MYSQL_HOST'] = '92.205.12.247'
app.config['MYSQL_USER'] = 'python_crud'
app.config['MYSQL_PASSWORD'] = 'python_crud'
app.config['MYSQL_DB'] = 'python_crud'

# Intialize MySQL
mysql = MySQL(app)


@app.route('/test')
def test():
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
                # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            session['password'] = account['password']


            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password!", "danger")
    return render_template('auth/login.html',title="Login")



# http://localhost:5000/pythinlogin/register 
# This will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        cursor.execute( "SELECT * FROM user WHERE username LIKE %s", [username] )
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash("Account already exists!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash("Username must contain only characters and numbers!", "danger")
        elif not username or not password or not email:
            flash("Incorrect username/password!", "danger")
        else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s)', (email,username, password))
            mysql.connection.commit()
            flash("You have successfully registered!", "success")
            return redirect(url_for('login'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!", "danger")
    # Show registration form with message (if any)
    return render_template('auth/register.html',title="Register")

# http://localhost:5000/pythinlogin/home 
# This will be the home page, only accessible for loggedin users

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
        import requests
        url = BASE_URL + 'everything?q=' + searchQuery + '&apiKey=' + API_KEY
        response = requests.get(url)
        data = response.json()

        first_article = data['articles'][0]
        three_articles = data['articles'][1:4]
                  
        return render_template('index.html',categories=categories, NewsCategory=NewsCategory ,username=session['username'],title="Homes", data=data, first_article=first_article, three_articles=three_articles)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))    


@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('auth/profile.html', username=session['username'],title="Profile")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))  



if __name__ =='__main__':
	app.run(debug=True)
