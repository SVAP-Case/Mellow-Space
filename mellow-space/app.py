from flask import Flask,redirect,url_for,render_template,request,session,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_mail import Mail, Message

app=Flask(__name__)
app.secret_key="it's_not_the_actual_one"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mellow.space.1@gmail.com'
app.config['MAIL_PASSWORD'] = 'zgczgaqggfmdirou'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_MAX_EMAILS']=1
mail = Mail(app)
db=SQLAlchemy(app)

class users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(100))
    last_name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    password=db.Column(db.String(100))

@app.route("/")
def home():
    return render_template("main_page.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        email=request.form["em"]
        pasw=request.form["pw"]
        found_user=users.query.filter_by(email=email).first()
        if found_user and check_password_hash(found_user.password,pasw):
            session["email"]=found_user.email
            return redirect(url_for("user"))
        else:
            flash("Invalid login credentials")
            return redirect(url_for("login"))
    else:
        if "email" in session:
            flash("Already logged in")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="POST":
        fname=request.form["nms"]
        lname=request.form["nmsl"]
        em=request.form["ems"]
        pas=request.form["pss"]
        for l in users.query.all():
            if em==l.email:
                flash("Account already present..")
                return redirect(url_for("login"))
        new_user=users(first_name=fname,last_name=lname,email=em,password=generate_password_hash(pas))
        db.session.add(new_user)
        db.session.commit()
        flash("Account created succesfully..Login now")
        return redirect(url_for("login"))
    else:
        if "email" in session:
            flash("Already logged in")
            return redirect(url_for("user"))
        return render_template("signup.html")

@app.route("/user",methods=["POST","GET"])
def user():
    email=None
    if "email" in session:
        email=session["email"]
        nm=users.query.filter_by(email=email).first()
        return render_template("user.html",usr=nm.first_name)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))

@app.route("/mood_test")
def mood_test():
    return render_template("mood_tester.html")

@app.route("/music")
def music():
    return render_template("music.html")

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/mailer")
def mailer():
    email=None
    if "email" in session:
        em=session["email"]
        msg = Message('Hello', sender = 'mellow.space.1@gmail.com', recipients = ['prackode@gmail.com'])
        msg.body = "Hello Flask message sent from Flask-Mail"
        mail.send(msg)
        flash("Mail Sent Succesfully...")
        return redirect(url_for("user"))
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "email" in session:
        flash("You have been logged out","info")
        session.pop("email",None)
    else:
        flash("No user logged in..")
    return redirect(url_for("login"))

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)