from flask_login import UserMixin
from watchlist import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin): # 设置数据库表，继承LoginUser
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))  # 密码机密加密储存

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password) # 直接检查哈希与字符串

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(6))


