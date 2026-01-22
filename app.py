from flask import Flask, render_template, redirect, url_for, request
from flask_login import (
    LoginManager, UserMixin,
    login_user, login_required, 
    logout_user, current_user
)

import Alphabot #creare

app = Flask(__name__)
app.secret_key = "ChiaveSegreta"

login_manager = LoginManager()
login_manager.init_app
login_manager.login_view = "login"

robot = Alphabot()


#classe con costruttore che ha id
class User(UserMixin):
    def __init__(self,id):
        self.id = id

USER = {
    "admin":{"password":"alphabot"}
}

def load_user(user_id):
    if user_id in USER:
        return User(user_id)
    return None

#Login
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]
        #query
        if username in USER and USER[username]["password"]:
            login_user(User(username))
            return redirect(url_for("control"))#control=pagina che muove, control è nome della funzione

    return render_template("login.html")

#Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

#pagina control
@app.route("/control")
@login_requiredù
def control():
    return render_template("control.html", user=current_user)

#movimento robot <cmd> dinamico
@app.route("/move/<cmd>")
@login_required
def move(cmd):
    if cmd == 