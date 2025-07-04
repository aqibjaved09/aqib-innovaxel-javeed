
from flask import Flask
import secrets
import validators
from flask import jsonify, request

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

#rd Addition
@app.route('/shorten', methods=['POST'])
def create_short_url():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    url = data['url']
    
    if not validators.url(url):
        return jsonify({'error': 'Invalid URL'}), 400
    
    short_code = secrets.token_urlsafe(6)[:6]
    
    while ShortURL.query.filter_by(short_code=short_code).first():
        short_code = secrets.token_urlsafe(6)[:6]
    
    new_url = ShortURL(url=url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()
    
    return jsonify({
        'id': new_url.id,
        'url': new_url.url,
        'shortCode': new_url.short_code,
        'createdAt': new_url.created_at,
        'updatedAt': new_url.updated_at
    }), 201

if __name__ == '__main__':
    app.run(debug=True)