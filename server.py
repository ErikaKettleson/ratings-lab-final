"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (connect_to_db, db, User, Rating, Movie)


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """ show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register_form')
def show_form():
    """ show form."""

    return render_template("register_form.html")


@app.route('/register_form', methods=["POST"])
def form_success():
    """ reroute home with email/pass."""

    email = request.form.get('email')
    password = request.form.get('password')

    # justto check if email alreayd in db & rerote to login
    # user = User.query.filter_by(email=email).one()

    if email != User.query.filter_by(email=email).all():
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("thanks for registering my friend")
        session["logged_in_user_email"] = user.user_id
        return redirect('/')

    else:
        # redirect them to the login page
        flash("welcome back my friend")
        #do login stuff
        return redirect('/login_form')



@app.route('/login_form')
def show_login_form():
    """ show login form."""

    return render_template("login_form.html")


@app.route('/login_form', methods=["POST"])
def user_login_form():
    """ show login form."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).one()
    if user.password == password:
        # redirect them to the login page
        flash("welcome back my friend")
        session["logged_in_user_email"] = user.user_id
        return redirect('/')

    # add an elif that would test the pasword match as well

    else:

        return redirect('/register_form.html')

@app.route("/logout_form")
def process_logout():
    """Log user out."""

    del session["logged_in_user_email"]
    flash("Logged out!")
    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
