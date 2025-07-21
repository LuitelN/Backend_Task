from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Blog Model
class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# GET all blogs
@app.route('/api/blogs', methods=['GET'])
def get_all_blogs():
    blogs = Blog.query.all()
    return jsonify([blog.to_dict() for blog in blogs])

# GET blog by ID
@app.route('/api/blogs/<int:blog_id>', methods=['GET'])
def get_blog_by_id(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return jsonify(blog.to_dict())

# POST - Create new blog
@app.route('/api/blogs', methods=['POST'])
def create_blog():
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['title', 'description', 'category']):
            return jsonify({'error': 'Missing required fields: title, description, category'}), 400
        
        new_blog = Blog(
            title=data['title'],
            description=data['description'],
            category=data['category']
        )
        
        db.session.add(new_blog)
        db.session.commit()
        
        return jsonify(new_blog.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PUT - Update blog
@app.route('/api/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    try:
        blog = Blog.query.get_or_404(blog_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'title' in data:
            blog.title = data['title']
        if 'description' in data:
            blog.description = data['description']
        if 'category' in data:
            blog.category = data['category']
        
        db.session.commit()
        return jsonify(blog.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Seed data (for testing)
@app.route('/api/blogs/seed', methods=['POST'])
def seed_data():
    Blog.query.delete()
    
    blogs = [
        Blog(title="Getting Started with Python", description="A beginner's guide to Python programming", category="Programming"),
        Blog(title="Web Development Basics", description="Learn HTML, CSS, and JavaScript fundamentals", category="Web Development"),
        Blog(title="Database Design Tips", description="Best practices for designing relational databases", category="Database")
    ]
    
    for blog in blogs:
        db.session.add(blog)
    
    db.session.commit()
    return jsonify({"message": "Sample data added successfully!"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)