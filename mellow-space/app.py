from flask import Flask,redirect,url_for,render_template,request,session,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)
app.secret_key="hello"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    password=db.Column(db.String(100))

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    complete=db.Column(db.Boolean)
    user=db.Column(db.Integer)

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
        name=request.form["nms"]
        em=request.form["ems"]
        pas=request.form["pss"]
        for l in users.query.all():
            if em==l.email:
                flash("Account already present..")
                return redirect(url_for("login"))
        new_user=users(name=name,email=em,password=generate_password_hash(pas))
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
        my_todo=Todo.query.filter_by(user=email).all()
        return render_template("user.html",todo_list=my_todo,usr=nm.name)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))

@app.route("/add",methods=["POST"])
def add():
    title=request.form.get("title")
    new_todo=Todo(title=title,complete=False,user=session["email"])
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("user"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo=Todo.query.filter_by(id=todo_id).first()
    todo.complete=not todo.complete
    db.session.commit()
    return redirect(url_for("user"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo=Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("user"))

@app.route("/game")
def game():
    return render_template("game.html")

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