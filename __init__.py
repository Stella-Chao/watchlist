# init
import os, sys

from flask import Flask # 引入Flask实例
from flask_sqlalchemy import SQLAlchemy  # 引入数据库实例
from flask_login import LoginManager  # 引入用户认证模块


# 确认sqlite的系统平台
WIN = sys.platform.startswith('win')
if WIN == 'win':
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__) # 实例化app， 声明flask程序实例

app.config['SECRET_KEY'] = 'dev'  # flask会话
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')  # 设置database的url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对数据库监控

db = SQLAlchemy(app)  # 由app实例化数据库
login_manager = LoginManager(app)  # 设置login_manager

login_manager.login_view = 'login' # 指定login的视图

@login_manager.user_loader  # user_loader装饰器，登入指定user_id
def load_user(user_id):  # 由ID查询返回user
    from models import User
    user = User.query.get(int(user_id))
    return user

@app.context_processor
def inject_user():
    from models import User
    user = User.query.first()
    return dict(user=user)   # 声明上下文，view视图中可直接使用



