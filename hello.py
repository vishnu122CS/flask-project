from flask import Flask,render_template,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#create a flask instance
app = Flask(__name__)
#add database
#old sqldb
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#new sql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://root:password123@localhost/our_users'
#secret key
app.config['SECRET_KEY']='my super secret key'
#initialize the database
db = SQLAlchemy(app)

#create model
class Users(db.Model):
     id = db.Column(db.Integer , primary_key = True)
     name = db.Column(db.String(200),nullable = False)
     email = db.Column(db.String(120),nullable = False, unique = True)
     date_added = db.Column(db.DateTime,default = datetime.utcnow)

    #create a string
     def __repr__(self):
          return '<Name %r>' % self.name
     
with app.app_context():
     db.create_all()

#create a form class
class UserForm(FlaskForm):
     name = StringField("Name",validators=[DataRequired()])
     email = StringField("Email",validators = [DataRequired()])
     submit = SubmitField("Submit")
#create a form class
class nameform(FlaskForm):
        name = StringField("whats your name", validators = [DataRequired()])
        submit = SubmitField("submit")


#create a route decorator


@app.route('/user/add',methods = ['GET','POST'])
def add_user():
        name = None
        form = UserForm()

        if form.validate_on_submit():
             user = Users.query.filter_by(email=form.email.data).first()
             if user is None:
                  user = Users(name=form.name.data, email=form.email.data)
                  db.session.add(user)
                  db.session.commit()
             name = form.name.data
             form.name.data = ""
             form.email.data = ""
             
             flash("user added successfully")
        
        our_users = Users.query.order_by(Users.date_added)    
        return render_template("add_user.html",form = form,name = name,our_users = our_users)

@app.route('/')
def index():
    first_name = "vishnu"
    stuff = "This is title Text"
    flash("Welcome to ur website!")
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

#create name page
@app.route('/name', methods = ['GET','POST'])
def name():
     name = None
     form = nameform()
     #validate form 
     if form.validate_on_submit():
          name = form.name.data
          form.name.data = ""
          flash("Form submitted successfully")
     return render_template("name.html",name = name ,form = form)
                           
