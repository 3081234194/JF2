"""
主要功能

主页面显示开关灯样式(图片按钮)
接受nodemcu请求并回复

实现方式

数据库记录commend date(方便以后log输出)
last_action如果为0，则灯处于可开状态，反之
commend 
"""

import datetime
import time
from os import urandom
from flask import Flask, render_template,url_for, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
app = Flask(__name__)
app.config.from_object("config")
app.secret_key = urandom(16)
db = SQLAlchemy(app)
###############ORM######################
class Device(db.Model):
    #指令id号
    id = db.Column(db.Integer,primary_key=True)
    #写入指令(可拓展并非只有on|off,调整指令请注意下面字节限制)
    commend = db.Column(db.String(5), nullable=False)
    #指令下达时间(用于回归方程|机器学习)
    date = db.Column(db.DateTime)
class Device_info():
    # 设备信息记录，同时便于认证设备(防止设备指令被非法获取)
    id = db.Column(db.String(),nullable=False)
    #移步dueros智能家居协议，设备类型
    type = db.Column(db.String(20))
    data = db.Column(db.DateTime)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    # 设置用户权限
    authority = db.Column(db.Integer, nullable=False)
############辅助函数################
def create_db():
    #重置化数据库
    db.drop_all()
    db.create_all()
    user = User(email="3081234194@qq.com", password="12345678",authority=1)
    user2 = Device(commend="off",date=datetime.datetime.now())
    db.session.add(user2)
    db.session.add(user)
    db.session.commit()
# 检查邮箱和密码是否匹配
def valid_login(email,password):
    user = User.query.filter(and_(User.email==email,User.password==password)).first()
    if user:
        return True
    else:
        return False
# 检查是否已经登陆(检查session)
def had_login():
    if session.get("email"):
        return True
    else:
        return False
# 写入cookie
def set_session(email):
    #开启session持久化存储
    session.permanent = True
    # 设置session到期时间
    app.permanent_session_lifetime = time.time()+60
    session["email"] = email

#控制界面
@app.route("/control")
def index():
    if had_login():
        #查询数据库中commend
        cl = Device.query.order_by(Device.id.desc()).first()#获取最新的指令
        commend = cl.commend
        print(commend)
        return render_template("control.html", commend=commend)
    else:
        error = "请先验证身份"
        return redirect(url_for("login",error=error))
#设备请求(不验证设备!)
@app.route("/ser/<status>",methods=["POST","GET"])
def ser(status):
    #查询数据库中commend
    cl = Device.query.order_by(Device.id.desc()).first()#获取最新的指令
    commend = cl.commend
    if status==commend:
        return "ok"
    else:
        return commend
#发送指令
@app.route("/server/<commend>")
def server(commend):
    if had_login():
        user = Device(commend=commend,date=datetime.datetime.now()) 
        db.session.add(user)
        db.session.commit()
        return redirect("/control")
    else:
        error = "请进行身份验证"
        return redirect(url_for("login",error=error))
@app.route("/login", methods=["POST","GET"])
def login():
    if request.args.get("error"):
        error = request.args.get("error")
    else:
        error = None
    if request.method == "POST":
        if valid_login(request.form['email'], request.form['password']):
            set_session(request.form.get('email'))
            return redirect("/control")
        else:
            error = '错误的用户名或密码！'

    return render_template('login.html', error=error)

# 3.注销
create_db()
app.run(debug=True,host="0.0.0.0")
