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
from flask import Flask, render_template,url_for, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
class Device(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    commend = db.Column(db.String(5), nullable=False)
    date = db.Column(db.DateTime)

def create_db():
    db.drop_all()
    db.create_all()
    user2 = Device(commend=1,date=datetime.datetime.now())
    db.session.add(user2)
    db.session.commit()
@app.route("/")
def index():
    #查询数据库中commend
    cl = Device.query.order_by(Device.id.desc()).first()#获取最新的指令
    commend = cl.commend
    print(commend)
    return render_template("index.html", commend=commend)

@app.route("/ser/<status>",methods=["POST","GET"])
def ser(status):
    #查询数据库中commend
    cl = Device.query.order_by(Device.id.desc()).first()#获取最新的指令
    commend = cl.commend
    if status==commend:
        return "ok"
    else:
        return str(commend)
@app.route("/server/<commend>")
def server(commend):
    user = Device(commend=commend,date=datetime.datetime.now()) 
    db.session.add(user)
    db.session.commit()
    return redirect("/")
create_db()
app.run(debug=True,host="0.0.0.0")
