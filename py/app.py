"""
主要功能

主页面显示开关灯样式(图片按钮)
接受nodemcu请求并回复

实现方式

数据库记录commend date(方便以后log输出)
last_action如果为0，则灯处于可开状态，反之
commend 
"""
from flask import Flask, render_template,url_for, rediect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
class Device(db.Model):
    id = db.Column(db.Integer primary_key=True)
    commend = db.Column(db.String(5), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
@app.route("/")
def index():
    #查询数据库中commend
    list = Device.qiery.filter(Device.commend)
    commend = list[-1]#获取最新的指令
    return render_template("index.html", commend=commend)

@app.route("/ser/<status>")
def ser(status):
    #查询数据库中commend
    list = Device.qiery.filter(Device.commend)
    commend = list[-1]#获取最新的指令
    if status==commend:
        return "ok"
    else:
        return commend
@app.route("/server/<commend>")
def server(commend):
    user = Device(commend=commend)
    db.session.add(user)
    db.session.commit()
    return rediect(url_for("/"))
