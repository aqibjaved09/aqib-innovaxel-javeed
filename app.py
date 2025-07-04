
from flask import Flask

# 2nd Addition

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    access_count = db.Column(db.Integer, default=0)

# Update the __main__ block:
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

app = Flask(__name__)

@app.route('/')
def home():
    return "URL Shortener Service"

if __name__ == '__main__':
    app.run(debug=True)