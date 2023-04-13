from watchlist import app
from flask import render_template

@app.errorhandler(404)
def page_no_found():
    from models import User
    return render_template('404.html'), 404
