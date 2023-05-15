from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
import sqlite3
from sqlalchemy import and_




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///My_db.sqlite3'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class User(db.Model):
    __tablename__ = 'user'
    user_fname=db.Column(db.String, nullable=False)
    user_lname=db.Column(db.String, nullable=False)
    user_email=db.Column(db.String, primary_key=True)
    user_password = db.Column(db.String, nullable = False)
    user_dob=db.Column(db.String, nullable = False)

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_fname=db.Column(db.String, nullable=False)
    admin_lname=db.Column(db.String, nullable=False)
    admin_email=db.Column(db.String, primary_key=True)
    admin_password = db.Column(db.String, nullable = False)
    admin_dob=db.Column(db.String, nullable = False)   

class Admin_Show_Management(db.Model):
    __tablename__ = 'admin_show_management_2'
    show_name=db.Column(db.String, nullable=False)
    show_id=db.Column(db.Integer, nullable=False, primary_key=True)
    show_rating=db.Column(db.Integer, nullable=False)
    show_tags = db.Column(db.String, nullable = False)
    ticket_price=db.Column(db.Integer, nullable = False) 
    show_capacity=db.Column(db.Integer, nullable=False)
    customer_feedback=db.Column(db.String, nullable=False)

class Admin_Venue_Management(db.Model):
     __tablename__ = 'admin_venue_management'
     venue_name=db.Column(db.String, nullable=False)
     venue_id=db.Column(db.Integer, nullable=False, primary_key=True)
     venue_capacity=db.Column(db.Integer, nullable=False)
     venue_place = db.Column(db.String, nullable = False)
    
class Bookings(db.Model):
     __tablename__ = 'bookings'
     venue_id=db.Column(db.Integer)
     user_email=db.Column(db.String,nullable=False, primary_key=True)



@app.route('/',methods=['GET'])
def login():
    return render_template("login.html")


@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template("user_signup.html")
    else:
        user=User(user_fname=request.form["user_fname"],user_lname=request.form["user_lname"],user_password=request.form["user_pass"],user_email=request.form["user_email"],user_dob=request.form["user_dob"])
        db.create_all()
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    
@app.route('/user_login',methods=['GET','POST'])
def User_Login():
    if request.method == 'GET':
        return render_template("user_login.html")
    else:
        username=request.form["user_email"]
        password=request.form["user_pass"]
        user=User.query.filter_by(user_password=password,user_email=username).first()
        if user is None:
            return render_template("authentication_error.html")
        else:
            return redirect("/"+username+"/start") 
        
@app.route('/admin_login',methods=['GET','POST'])
def Admin_Login():
    if request.method == 'GET':
        return render_template("admin_login.html")
    else:
        username=request.form["admin_email"]
        password=request.form["password"]
        if username=='2005521@kiit.ac.in' and password=='1234':
            return redirect("/admin_start") 
        else:
            return render_template("authentication_error.html")
            
        
@app.route('/<username>/start',methods=['GET'])
def home(username):
    user=User.query.filter_by(user_email=username).first()
    booking=Bookings.query.filter_by(user_email=username).first()
    # follow=[]
    # for i in booking:
    #     follow+=[Admin_Show_Management.query.filter_by(show_id=i.venue_id).all()]
    follow=Admin_Show_Management.query.all()
    # print(follow[0])
    if request.method == "GET":
       return render_template("user_profile.html", users=user,posts=follow,b=booking)
    
@app.route('/admin_start',methods=['GET'])
def home1():
    if request.method == "GET":
       a=len(Admin_Venue_Management.query.all())
       b=len(Admin_Show_Management.query.all())
       venue=Admin_Venue_Management.query.all()
       show=Admin_Show_Management.query.all()
       return render_template("admin_profile.html",admin_venue=a,admin_show=b,venue=venue,show=show)
      
@app.route('/<username>/delete2/<post_id>',methods=['GET','POST'])
def delete2(username,post_id):
    if request.method=='GET':
        post=Bookings.query.filter(and_(Bookings.venue_id.like(int(post_id)), Bookings.user_email.like(username))).first()
        # Admin_Show_Management.query.filter(or_(Admin_Show_Management.show_name.like(search))).all()
        db.session.delete(post)
        db.session.commit()
        return redirect("/"+username+"/start") 

@app.route('/<username>/update',methods=['GET','POST'])
def update_user(username):
    if request.method=='GET':
        user = User.query.filter_by(user_email=username).first()
        return render_template("update_user_info.html",users=user)
    elif request.method=='POST':
        user=User.query.filter_by(user_email=username).first()
        if request.form.get("user_fname")!='':
            user.fname=request.form.get("user_fname")
        if request.form.get("user_lname")!='':
            user.lname=request.form.get("user_lname")
        if request.form.get("email")!='':
            user.email=request.form.get("user_email")
        if request.form.get("pass")!='':
            user.password=request.form.get("user_pass")
        if request.form.get("user_dob")!='':
            user.dob=request.form.get("user_dob")
        db.session.commit()
        return redirect("/"+username+"/home")      


@app.route('/show_management',methods=['GET','POST'])
def show_management():
    if request.method=='GET':
        return render_template("admin_show_management.html")
    elif request.method=='POST':
        show=Admin_Show_Management(show_name=request.form["sname"],show_id=int(request.form["sid"]),show_rating=int(request.form["srating"]),show_tags=request.form["stag"],ticket_price=int(request.form["sprice"]),show_capacity=int(request.form["scap"]),customer_feedback=" ")
        db.create_all()
        db.session.add(show)
        db.session.commit()
        return redirect("/admin_start") 
    
@app.route('/venue_management',methods=['GET','POST'])
def venue_management():
    if request.method=='GET':
        return render_template("admin_venue_management.html")
    elif request.method=='POST':
        venue=Admin_Venue_Management(venue_name=request.form["pname"],venue_id=int(request.form["pdescription"]),venue_capacity=int(request.form["ptag"]),venue_place=request.form["prating"])
        db.create_all()
        db.session.add(venue)
        db.session.commit()
        return redirect("/admin_start")
    

@app.route('/delete/<post_id>',methods=['GET','POST'])
def delete(post_id):
    if request.method=='GET':
        post=Admin_Venue_Management.query.filter_by(venue_id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        return redirect("/admin_start")
    
@app.route('/update/<post_id>',methods=['GET','POST'])
def update(post_id):
    if request.method=='GET':
        post=Admin_Venue_Management.query.filter_by(venue_id=post_id).first()
        return render_template('change_venue.html',post=post)
    if request.method=='POST':
        post=Admin_Venue_Management.query.filter_by(venue_id=post_id).first()
        if request.form.get("pname")!='':
            post.venue_name=request.form.get("pname")
        if request.form.get("pplace")!='':
            post.venue_place=request.form.get("pplace")
        if request.form.get("pcapacity")!='':
            post.venue_capacity=request.form.get("pcapacity")
        db.session.commit()
        return redirect("/admin_start")
    
@app.route('/delete1/<post_id>',methods=['GET','POST'])
def delete1(post_id):
    if request.method=='GET':
        post=Admin_Show_Management.query.filter_by(show_id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        return redirect("/admin_start")

@app.route('/update1/<post_id>',methods=['GET','POST'])
def update1(post_id):
    if request.method=='GET':
        post=Admin_Show_Management.query.filter_by(show_id=post_id).first()
        return render_template('change_show.html',post=post)
    if request.method=='POST':
        post=Admin_Show_Management.query.filter_by(show_id=post_id).first()
        if request.form.get("pname")!='':
            post.show_name=request.form.get("pname")
        if request.form.get("prating")!='':
            post.show_rating=request.form.get("prating")
        if request.form.get("ptag")!='':
            post.show_tags=request.form.get("ptag")
        if request.form.get("pcapacity")!='':
            post.show_capacity=request.form.get("pcapacity")
        if request.form.get("pprice")!='':
            post.ticket_price=request.form.get("pprice")
        db.session.commit()
        return redirect("/admin_start")

    
@app.route('/<username>/new_post',methods=['GET','POST'])
def new_post(username):
    if request.method=='GET':
        user = User.query.filter_by(user_email=username).first()
        return render_template("find_show.html",users=user)
    elif request.method=='POST':
        search=request.form.get("search")
        result=Admin_Show_Management.query.filter(or_(Admin_Show_Management.show_name.like(search),Admin_Show_Management.show_id.like(search),Admin_Show_Management.show_rating.like(search))).all()
        if len(result)==0:
            search=search.capitalize()
            user = User.query.filter_by(user_email=username).first()
            return render_template("no_show.html",users=user)
        else:
            user = User.query.filter_by(user_email=username).first()
            return render_template('result.html',users=user,result=result)

@app.route('/<username>/follow/<item>',methods=['GET','POST'])
def follow(username,item):
    if request.method=='GET':
        follow=Bookings(venue_id=item,user_email=username)
        db.session.add(follow)
        db.session.commit()
        show=Admin_Show_Management.query.filter_by(show_id=item).first()
        if show.show_capacity==0:
            return render_template('housefull.html')
        show.show_capacity=show.show_capacity-1
        db.session.commit()
        return redirect('/'+username+'/start')

@app.route('/<username>/feedback/<item>',methods=['GET','POST'])
def feedback(username,item):
    if request.method=='GET':
        user = User.query.filter_by(user_email=username).first()
        post=Admin_Show_Management.query.filter_by(show_id=item).first()
        return render_template('show_feedback.html',users=user,posts=post) 
    else:
        a=request.form.get("fname")
        user = User.query.filter_by(user_email=username).first()
        post=Admin_Show_Management.query.filter_by(show_id=item).first()
        post.customer_feedback=a
        db.session.commit()
        return redirect("/"+username+"/start")  




    


if __name__=="__main__":
    app.run(debug=True)