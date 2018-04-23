from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------------------------------------------------- #

class Site(db.Model):
    """Scraped Sites Cache"""

    __tablename__ = "sites"

    site_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url =  db.Column(db.String(100), nullable=False)
    html =  db.Column(db.Text, nullable=False)

    def __repr__(self):
        """print info in useful form"""
        return "<Site {}, id={}>".format(self.url, self.site_id)

# ------------------------------------------------------ #

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///sites"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
