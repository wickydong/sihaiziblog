#! /usr/bin/python
# -*- coding:utf-8 -*-
# author: i@sihaizi.com

#账号存放于user_message库的user中!

from flask import Flask,render_template,url_for,request,session,redirect
import MySQLdb
from flaskext.mysql import MySQL
import sys
reload(sys)
sys.setdefaultencoding('utf8')
mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
#app.config['MYSQL_DATABASE_DB'] = 'user_message'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = "\xdd\xe6\x1c\x9b2K\x10I\x1d\x03\xed~\xdadr\xb21\xac!\x89\x0c\xc4\x15`"
mysql.init_app(app)

@app.route("/admin")
def admin():
    return render_template("login.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST" or request.method == "GET":
        cursor = mysql.get_db().cursor()
        cursor.execute("use user_message")
        cursor.execute("select user,passwd from user where id=1")
        user,passwd =  cursor.fetchall()[0]
        user = str(user) 
        passwd = str(passwd)
        if request.form["user"] == user and request.form["passwd"] == passwd:
            session["user"] = user
            return redirect(url_for("edit.html"))
        else:
            return render_template("login.html",mess="failed")
        cursor.close()

@app.route("/")
def index():
    cursor = mysql.get_db().cursor()
    cursor.execute("use sihaizi")
    cursor.execute("select title,article,author,date from blog")
    print cursor.fetchall()
    return render_template("index.html")
@app.route("/sx")
def sx():
    return render_template("sx.html")

@app.route("/about")
def about():
    return render_template("about.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
