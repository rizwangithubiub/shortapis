from flask import Flask, request, jsonify, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import re
from urllib.parse import urlparse

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    access_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': str(self.id),
            'url': self.url,
            'shortCode': self.short_code,
            'createdAt': self.created_at.isoformat() + 'Z',
            'updatedAt': self.updated_at.isoformat() + 'Z'
        }

    def to_dict_with_stats(self):
        data = self.to_dict()
        data['accessCount'] = self.access_count
        return data

# Utility functions
def generate_short_code(length=6):
    """Generate a random short code"""
    characters = string.ascii_letters + string.digits
    while True:
        short_code = ''.join(random.choice(characters) for _ in range(length))
        if not URL.query.filter_by(short_code=short_code).first():
            return short_code

def is_valid_url(url):
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def validate_url_input(data):
    """Validate URL input data"""
    if not data:
        return False, "Request body is required"
    
    if 'url' not in data:
        return False, "URL field is required"
    
    url = data['url']
    if not url or not isinstance(url, str):
        return False, "URL must be a non-empty string"
    
    if not is_valid_url(url):
        return False, "Invalid URL format"
    
    return True, None

# API Endpoints

@app.route('/shorten', methods=['POST'])
def create_short_url():
    """Create a new short URL"""
    try:
        data = request.get_json()
        
        # Validate input
        is_valid, error_message = validate_url_input(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Generate unique short code
        short_code = generate_short_code()
        
        # Create new URL entry
        new_url = URL(
            url=data['url'],
            short_code=short_code
        )
        
        db.session.add(new_url)
        db.session.commit()
        
        return jsonify(new_url.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    """Retrieve original URL from short code"""
    try:
        url_entry = URL.query.filter_by(short_code=short_code).first()
        
        if not url_entry:
            return jsonify({'error': 'Short URL not found'}), 404
        
        return jsonify(url_entry.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/shorten/<short_code>', methods=['PUT'])
def update_short_url(short_code):
    """Update existing short URL"""
    try:
        url_entry = URL.query.filter_by(short_code=short_code).first()
        
        if not url_entry:
            return jsonify({'error': 'Short URL not found'}), 404
        
        data = request.get_json()
        
        # Validate input
        is_valid, error_message = validate_url_input(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Update URL
        url_entry.url = data['url']
        url_entry.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(url_entry.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_short_url(short_code):
    """Delete existing short URL"""
    try:
        url_entry = URL.query.filter_by(short_code=short_code).first()
        
        if not url_entry:
            return jsonify({'error': 'Short URL not found'}), 404
        
        db.session.delete(url_entry)
        db.session.commit()
        
        return '', 204
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/shorten/<short_code>/stats', methods=['GET'])
def get_url_statistics(short_code):
    """Get statistics for a short URL"""
    try:
        url_entry = URL.query.filter_by(short_code=short_code).first()
        
        if not url_entry:
            return jsonify({'error': 'Short URL not found'}), 404
        
        return jsonify(url_entry.to_dict_with_stats()), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

# Redirect endpoint (bonus feature)
@app.route('/<short_code>')
def redirect_to_original(short_code):
    """Redirect to original URL and increment access count"""
    try:
        url_entry = URL.query.filter_by(short_code=short_code).first()
        
        if not url_entry:
            return jsonify({'error': 'Short URL not found'}), 404
        
        # Increment access count
        url_entry.access_count += 1
        db.session.commit()
        
        return redirect(url_entry.url)
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

# Simple frontend (bonus feature)
@app.route('/')
def index():
    """Simple frontend interface"""
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>URL Shortener</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0; }
            input[type="text"] { width: 300px; padding: 10px; margin: 10px; }
            button { padding: 10px 20px; margin: 10px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .result { margin: 20px 0; padding: 15px; background: #d4edda; border: 1px solid #c3e6cb; border-radius: 5px; }
            .error { margin: 20px 0; padding: 15px; background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>URL Shortener Service</h1>
        
        <div class="container">
            <h2>Shorten URL</h2>
            <input type="text" id="urlInput" placeholder="Enter URL to shorten" />
            <button onclick="shortenUrl()">Shorten</button>
            <div id="shortenResult"></div>
        </div>
        
        <div class="container">
            <h2>Get Original URL</h2>
            <input type="text" id="shortCodeInput" placeholder="Enter short code" />
            <button onclick="getOriginalUrl()">Get Original</button>
            <div id="originalResult"></div>
        </div>
        
        <div class="container">
            <h2>Get Statistics</h2>
            <input type="text" id="statsCodeInput" placeholder="Enter short code for stats" />
            <button onclick="getStats()">Get Stats</button>
            <div id="statsResult"></div>
        </div>

        <script>
            async function shortenUrl() {
                const url = document.getElementById('urlInput').value;
                const resultDiv = document.getElementById('shortenResult');
                
                if (!url) {
                    resultDiv.innerHTML = '<div class="error">Please enter a URL</div>';
                    return;
                }
                
                try {
                    const response = await fetch('/shorten', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ url: url })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        resultDiv.innerHTML = `
                            <div class="result">
                                <strong>Short URL Created!</strong><br>
                                Short Code: ${data.shortCode}<br>
                                Short URL: <a href="/${data.shortCode}" target="_blank">${window.location.origin}/${data.shortCode}</a><br>
                                Original URL: ${data.url}<br>
                                Created: ${data.createdAt}
                            </div>
                        `;
                    } else {
                        resultDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
                }
            }
            
            async function getOriginalUrl() {
                const shortCode = document.getElementById('shortCodeInput').value;
                const resultDiv = document.getElementById('originalResult');
                
                if (!shortCode) {
                    resultDiv.innerHTML = '<div class="error">Please enter a short code</div>';
                    return;
                }
                
                try {
                    const response = await fetch(`/shorten/${shortCode}`);
                    const data = await response.json();
                    
                    if (response.ok) {
                        resultDiv.innerHTML = `
                            <div class="result">
                                <strong>Original URL Found!</strong><br>
                                Original URL: <a href="${data.url}" target="_blank">${data.url}</a><br>
                                Short Code: ${data.shortCode}<br>
                                Created: ${data.createdAt}<br>
                                Updated: ${data.updatedAt}
                            </div>
                        `;
                    } else {
                        resultDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
                }
            }
            
            async function getStats() {
                const shortCode = document.getElementById('statsCodeInput').value;
                const resultDiv = document.getElementById('statsResult');
                
                if (!shortCode) {
                    resultDiv.innerHTML = '<div class="error">Please enter a short code</div>';
                    return;
                }
                
                try {
                    const response = await fetch(`/shorten/${shortCode}/stats`);
                    const data = await response.json();
                    
                    if (response.ok) {
                        resultDiv.innerHTML = `
                            <div class="result">
                                <strong>URL Statistics</strong><br>
                                URL: <a href="${data.url}" target="_blank">${data.url}</a><br>
                                Short Code: ${data.shortCode}<br>
                                Access Count: ${data.accessCount}<br>
                                Created: ${data.createdAt}<br>
                                Updated: ${data.updatedAt}
                            </div>
                        `;
                    } else {
                        resultDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
                }
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_template)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Initialize database and create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)