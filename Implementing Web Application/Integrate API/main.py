from flask import Flask, render_template, request, redirect, url_for, session,flash
import re
import random
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e'


@app.route('/test')
def test():
    return render_template('index.html')


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
