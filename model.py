"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions
# reference user_id and movie_id in other columns?
class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(264), nullable=True)
    password = db.Column(db.String(264), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    ratings = db.relationship('Rating')

    def __repr__(self):
        """ representation when printed user id & email"""
        return "<User user_id=%s email=%s zipcode=%s>" % (self.user_id, self.email, self.zipcode)


class Rating(db.Model):
    """just ratings ."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    movie = db.relationship('Movie')
    user = db.relationship('User')

    def __repr__(self):
        return "<Rating rating_id=%s user_id=%s movie_id=%s score=%s>" % (self.rating_id, self.user_id, self.movie_id, self.score)


class Movie(db.Model):
    """just movies ."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    released_at = db.Column(db.DateTime, nullable=True)
    title = db.Column(db.String(264), nullable=False)
    imdb_url = db.Column(db.String(256), nullable=True)

    ratings = db.relationship('Rating')

    def __repr__(self):
        """ representation when printed user id & email"""
        return "<Movie movie_id=%s title=%s released_at=%s>" % (self.movie_id, self.title, self.released_at)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
