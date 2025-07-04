
from flask import Flask
import secrets
import validators
from flask import jsonify, request
from flask import redirect

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


# 4th Addition 
@app.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    url_entry = ShortURL.query.filter_by(short_code=short_code).first()
    
    if not url_entry:
        return jsonify({'error': 'URL not found'}), 404
    
    url_entry.access_count += 1
    db.session.commit()
    
    return jsonify({
        'id': url_entry.id,
        'url': url_entry.url,
        'shortCode': url_entry.short_code,
        'createdAt': url_entry.created_at,
        'updatedAt': url_entry.updated_at
    }), 200

# 5th Addtion 

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url_entry = ShortURL.query.filter_by(short_code=short_code).first()
    
    if not url_entry:
        return jsonify({'error': 'URL not found'}), 404
    
    url_entry.access_count += 1
    db.session.commit()
    
    return redirect(url_entry.url, code=301)

# 6th additon

@app.route('/shorten/<short_code>', methods=['PUT'])
def update_url(short_code):
    url_entry = ShortURL.query.filter_by(short_code=short_code).first()
    
    if not url_entry:
        return jsonify({'error': 'URL not found'}), 404
    
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    new_url = data['url']
    
    if not validators.url(new_url):
        return jsonify({'error': 'Invalid URL'}), 400
    
    url_entry.url = new_url
    db.session.commit()
    
    return jsonify({
        'id': url_entry.id,
        'url': url_entry.url,
        'shortCode': url_entry.short_code,
        'createdAt': url_entry.created_at,
        'updatedAt': url_entry.updated_at
    }), 200

if __name__ == '__main__':
    app.run(debug=True)