#! /usr/bin/python
# -*- coding:utf-8 -*-
# author: i@sihaizi.com

#账号存放于user_message库的user中!

from flask import Flask,render_template,url_for,request,session,redirect
import MySQLdb
from datetime import *
from flaskext.mysql import MySQL
import sys
reload(sys)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
sys.setdefaultencoding('utf8')
mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
#app.config['MYSQL_DATABASE_DB'] = 'user_message'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = "\xdd\xe6\x1c\x9b2K\x10I\x1d\x03\xed~\xdadr\xb21\xac!\x89\x0c\xc4\x15`"
mysql.init_app(app)

@app.route("/admin")  #管理员后台
def admin():
    return render_template("login.html")

@app.route("/login",methods=["GET","POST"]) #验证登陆，进入后台编辑
def login():
    if request.method == "POST" or request.method == "GET":
        cursor = mysql.get_db().cursor()
        cursor.execute("use user_message")
        cursor.execute("select user,passwd from user where id=0")
        user,passwd =  cursor.fetchall()[0]
        user = str(user) 
        passwd = str(passwd)
        if request.form["user"] == user and request.form["passwd"] == passwd:
            session["user"] = user
            return render_template("edit.html",user=user)
        else:
            return render_template("login.html",mess="failed")
        cursor.close()

@app.route("/logout") #退出后台
def logout():
    session.pop("user",None)
    return redirect(url_for("index"))

@app.route("/edit") #后台选择操作
def edit():
    if "user" in session:
        cho = request.args.get("chose")
        user = request.args.get("user")
        if cho == "write":
            return render_template("write.html",user=user)

@app.route("/write",methods=["POST"])
def write():
    times = str(date.today())
    title = str(request.form["title"])
    content = str(request.form["content"])
    user = str(request.form["user"])
#    user = request.args.get("user")
 #   print user
    cursor = mysql.get_db().cursor()
    cursor.execute("use sihaizi")
    #cursor.execute("insert into blog(title,article,author,date) values(%s,%s,%s,%s)" %(title,content,user,times))
    if request.files["img"]:
        f = request.files["img"]
        f.save("static/"+ times)
        imgurl = "static/" +times
        sql = "insert into blog(title,article,author,date,imgurl) values('%s','%s','%s','%s','%s')" %(title,content,user,times,imgurl)
    else:
        sql = "insert into blog(title,article,author,date) values('%s','%s','%s','%s')" %(title,content,user,times)
    cursor.execute(sql)
    mysql.get_db().commit()
    cursor.close()
    return redirect(url_for("index"))
@app.route("/")  #首页
def index():
    number = 0
    if request.args.get("start"):
        start = request.args.get("start")
        number = (int(start) - 1) * 10
    cursor = mysql.get_db().cursor()
    cursor.execute("use sihaizi")
    cursor.execute("select title,article,author,date,imgurl,id from blog order by id desc limit %s,10" %number)
    mess = cursor.fetchall()
    cursor.execute("select count(1) from blog")
    idsum = cursor.fetchall()
    idsum = idsum[0][0]
    if int(idsum) % 10 == 0:
        page = int(idsum) / 10
    else:
        page = int(idsum) / 10 + 1
    return render_template("index.html",mess=mess,page=page)#,autoescape=True)

@app.route("/links")
def links():
    return render_template("links.html")
@app.route("/talk")
def talk():
    title = str(request.args.get("title"))
    cursor = mysql.get_db().cursor()
    cursor.execute("use sihaizi")
    cursor.execute("select article,author,date,imgurl,id from blog where title='%s'" %title)
    mess = cursor.fetchall()
    return render_template("talk.html",mess=mess,title=title)
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
