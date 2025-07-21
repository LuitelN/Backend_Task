from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # change to your MySQL username
app.config['MYSQL_PASSWORD'] = 'Password12!'  
app.config['MYSQL_DB'] = 'blog_db'  

mysql = MySQL(app)

# Route: GET all blogs
@app.route('/blogs', methods=['GET'])
def get_blogs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM blogs")
    rows = cur.fetchall()
    cur.close()

    blogs = []
    for row in rows:
        blogs.append({
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'category': row[3]
        })
    return jsonify(blogs), 200

# Route: GET blog by ID
@app.route('/blogs/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM blogs WHERE id = %s", (blog_id,))
    row = cur.fetchone()
    cur.close()

    if row:
        blog = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'category': row[3]
        }
        return jsonify(blog), 200
    else:
        return jsonify({'error': 'Blog not found'}), 404

# Route: POST blog
@app.route('/blogs', methods=['POST'])
def create_blog():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    category = data.get('category')

    if not title or not category:
        return jsonify({'error': 'Title and Category are required'}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO blogs (title, description, category) VALUES (%s, %s, %s)",
                (title, description, category))
    mysql.connection.commit()
    new_id = cur.lastrowid
    cur.close()

    return jsonify({
        'id': new_id,
        'title': title,
        'description': description,
        'category': category
    }), 201

# Route: PUT blog
@app.route('/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    category = data.get('category')

    if not title or not category:
        return jsonify({'error': 'Title and Category are required'}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM blogs WHERE id = %s", (blog_id,))
    if not cur.fetchone():
        cur.close()
        return jsonify({'error': 'Blog not found'}), 404

    cur.execute("UPDATE blogs SET title = %s, description = %s, category = %s WHERE id = %s",
                (title, description, category, blog_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({
        'id': blog_id,
        'title': title,
        'description': description,
        'category': category
    }), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)  # default port = 5000
