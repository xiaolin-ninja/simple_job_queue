from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------------------------------------------------- #

class Sites(db.Model):
    """Web Scraping Task"""

    __tablename__ = "users"

    site_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url =  db.Column(db.String(100), nullable=False)
    html =  db.Column(db.String(600), nullable=False)

    def __repr__(self):
        """print info in useful form"""
        return "<Site {}, id={}>".format(self.url, self.site_id)

# ------------------------------------------------------ #

def connect_to_db(app, db_uri="postgresql:///jobs"):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")