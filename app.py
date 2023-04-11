import os, sys
import click

from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy

# 识别系统，设定sqlite
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# 实例化flask
app = Flask(__name__)

# 设定app.config
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'


# 声明数据库
db = SQLAlchemy(app)

# 声明数据的格式，使用db Model生成格式
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(6))



name = 'Sun Zhao'
# movies = [
#     {'title': 'My Neighbor Totoro', 'year': '1988'},
#     {'title': 'Dead Poets Society', 'year': '1989'},
#     {'title': 'A Perfect World', 'year': '1993'},
#     {'title': 'Leon', 'year': '1994'},
#     {'title': 'Mahjong', 'year': '1996'},
#     {'title': 'Swallowtail Butterfly', 'year': '1996'},
#     {'title': 'King of Comedy', 'year': '1999'},
#     {'title': 'Devils on the Doorstep', 'year': '1999'},
#     {'title': 'WALL-E', 'year': '2008'},
#     {'title': 'The Pork of Music', 'year': '2012'},
# ]

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)  # 声明上下文user

# 添加电影数据
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        title = request.form.get('title')
        year = request.form.get('year')
        # 验证数据
        if not title or not year or (len(year)>4) or len(title) > 60:
            flash('Invalid input')
            return redirect(url_for('index'))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created ')
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html',  movies=movies)

# 编辑电影数据，删除电影数据
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or (len(year)>4) or len(title) > 60:
            flash('Invalid input')
            return redirect(url_for('index'))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item Updated.')
        return render_template(url_for('index'))
    return redirect('edit.html', movie=movie)  # 传入被编辑的电影记录

# delete item
@app.route('/movie/delete/<int:movie_id>', methods=['GET', 'POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item delete.')
    return redirect(url_for('index'))



@app.errorhandler(404)
def page_no_found(e):
    user = User.query.first()
    return render_template('404.html'), 404

@app.cli.command()
def forge():
    db.create_all()

    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('done! ')

