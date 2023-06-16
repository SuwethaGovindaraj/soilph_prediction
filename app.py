import numpy as np
import pandas as pd
from flask import Flask, request, render_template,redirect,url_for
import joblib
from flask_mysqldb import MySQL



#Creating the flask app
app = Flask(__name__)

model = joblib.load(r"C:\Users\SUWETHA\Documents\soilph\soilph.pkl")

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'phpredict'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)
@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/loginpage')
def login():
    
        return render_template('login.html')

@app.route('/buttonpage')
def button():
    
        return render_template('button.html')

@app.route('/predictpage')
def pre():
    
        return render_template('soilph.html')

@app.route('/registerpage')
def reg():
    
        return render_template('registration.html')


# Register page
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/logout')
def logout():
    return render_template('home.html')

@app.route('/abtus')
def abtus():
    return render_template('abtuss.html')

# Login verification
@app.route('/login', methods=['POST'])
def login_verification():
    username = request.form['username']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    if user:
        # User exists, login successful
        return render_template('button.html')
    else:
        # User does not exist or password is incorrect, show error message
        return render_template('login.html', color='red' ,msg='Invalid username or password')


# Registration verification
@app.route('/register', methods=['POST'])
def register_verification():
    username = request.form['username']
    password = request.form['password']
    email= request.form['email']
    country = request.form['country']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password,email,country) VALUES (%s, %s ,%s,%s)", (username, password,email,country))
    mysql.connection.commit()
    cur.close()
    return render_template('login.html')



@app.route('/predict', methods=['GET','POST'])
def input():
    if request.method=="POST":
        details=request.form
        temperature=details['temperature']
        humidity=details['humidity']
        rainfall=details['rainfall']
        n=details['n']
        p=details['p']
        k=details['k']
        
        pred=model.predict([[temperature,humidity,rainfall,n,p,k]])
        # result = pred
        print(pred)
    

        if (pred[0] <=4 ):
            return render_template('result.html', prediction_text='Ph of the soil is {}.     Crops Recommended : Blueberries , Azaleas , Rhododendrons , Camellias , Potatoes (acidic soil varieties)'.format(pred))

        elif (pred[0] >4 and pred[0]<=5):
            return render_template('result.html', prediction_text='Ph of the soil is {}.     Crops Recommended :Cranberries , Raspberries , Strawberries , Currants , Potatoes (slightly acidic soil varieties)'.format(pred))
        
        elif (pred[0] >5 and pred[0]<=6):
            return render_template('result.html', prediction_text='Ph of the soil is {}.     Crops Recommended :Corn , Tomatoes , Squash , Cucumbers , Carrots , Peppers'.format(pred))

        elif (pred[0] >6 and pred[0]<=7):
            return render_template('result.html', prediction_text='Ph of the soil is {}.     Crops Recommended :Beans , Beets , Broccoli , Cabbage , Cauliflower , Lettuce'.format(pred))

        else:
            return render_template('result.html', prediction_text='Ph of the soil is {}.     Crops Recommended :Spinach , Radishes , Garlic , Onions , Peas'.format(pred))


if __name__ == '__main__':
    app.run(debug=True)

