from flask import Flask,render_template

#create a flask instance
app = Flask(__name__)

#create a route decorator
@app.route('/')

def index():
    first_name = "vishnu"
    stuff = "This is title Text"
    favourite_pizza = ["pepperoni","cheese","butter"]
    return render_template("index.html",first_name = first_name,stuff = stuff
                           ,favourite_pizza = favourite_pizza)

#localhost:5000/user/vishnu
@app.route('/user/<name>')

def user(name):
    return render_template("user.html",user_name = name)

#create custom error pages

#invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
