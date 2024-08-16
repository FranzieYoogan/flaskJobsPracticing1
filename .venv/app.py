
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session  # Correct import for Flask session management
import pymongo

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)    

@app.route("/", methods=['GET','POST'])
def login():
    ok = ""
    docs = []
    if request.method == "POST":
    
        email = request.form['email']
        password = request.form['password']


        if email and password:
                
            myclient = pymongo.MongoClient("mongodb+srv://franzieyoogan2:admin357159@cluster0.guw8a4s.mongodb.net/")
            mydb = myclient["jobs"]
            mycol = mydb["users"]

            mydoc = mycol.find().sort("name")

            docs = list(mydoc)
            for x in docs:
                if(x.get('userEmail') == email and x.get('userPassword') == password):
                    session["name"] = x.get('userName')
                    return redirect(url_for('dashboard'))
                
                
            ok ="sheesh"

 
        return render_template('index.htm',ok = ok)

    return render_template('index.htm')

@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
 
 if(request.method == "POST"):

    search = request.form['search']

    if search:
       myclient = pymongo.MongoClient("mongodb+srv://franzieyoogan2:admin357159@cluster0.guw8a4s.mongodb.net/")
       mydb = myclient["jobs"]
       mycol = mydb["jobs"]

       for x in mycol.find({"area": search}):
        print(x)


    return render_template('dashboard.htm',x = x)
 
 return render_template('dashboard.htm') 



@app.route("/signout", methods=['GET','POST'])
def signout():

 session["name"] = None

 return render_template('index.htm')

if __name__ == "__main__":
    app.run(debug = True)