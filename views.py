from flask import url_for, redirect, request, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user

from watchlist import app, db
from watchlist.models import User, Movie

@app.route('/', motheds=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form.get('title')
        year = request.form.get('year')
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created ')
        return redirect(url_for('index'))

    movies = Movie.query.all()  # 定义电影
    return render_template('index.html', movies=movies)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input. ')
            return redirect(url_for('login'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            logout_user(user)
            flash('Success login. ')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))
    return render_template('login.html')  # login

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect('index')

# edit data
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 修改当前的movie信息
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item update! ')
        return redirect(url_for('index'))

    return redirect('edit.html', movie=movie)

# delete data
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Delete item! ')
    return redirect(url_for('index'))

# settings
@app.route('/settings', methods=['POST', 'GET'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('Setting update! ')
        return redirect(url_for('index'))


    return render_template('settings.html')
