# 📝 Blog API with FastAPI

A simple and scalable RESTful API for managing blog posts and categories built with **FastAPI**, **SQLAlchemy**, and **SQLite**. This API supports creating, reading, and updating blog posts with category management.

---

## 📁 Features

- Create and update blog posts with category handling  
- Auto-create categories if they don’t exist  
- Retrieve all blogs or a single blog by ID  
- SQLite database (easy to swap with other databases)
- Pydantic models for request validation and response schema
- SQLAlchemy ORM for database interaction
- Postman Collection included for easy testing

---

## 📦 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework  
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit and ORM  
- [SQLite](https://www.sqlite.org/) - Lightweight relational DB (used for local development)  
- [Pydantic](https://docs.pydantic.dev/) - Data validation and settings management

---

## 🚀 Getting Started

### 1. **Clone the repository**
```bash
git clone https://github.com/<your-username>/fastapi-blog-api.git
cd fastapi-blog-api
```

### 2. **Create a virtual environment and activate it**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Unix/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Run the application**
```bash
uvicorn main:app --reload
```

The API will be live at:  
📍 `http://127.0.0.1:8000`

---

## 📬 API Endpoints

### ✅ Get All Blogs  
`GET /blogs`  
Returns a list of all blogs.

### ✅ Get Blog by ID  
`GET /blogs/{blog_id}`  
Returns a specific blog with its category.

### ✅ Create Blog  
`POST /blogs`  
Creates a blog. If the category does not exist, it is automatically created.

**Sample Body**
```json
{
  "title": "My First Blog",
  "description": "This is a test blog.",
  "category_name": "Tech"
}
```

### ✅ Update Blog  
`PUT /blogs/{blog_id}`  
Updates a blog and reassigns a category if needed.

---

## 📂 Database Models

### Blog
- `id`: int
- `title`: str
- `description`: str
- `category_id`: int

### Category
- `id`: int
- `name`: str

---

## 🧪 Postman Collection

You can test the API using Postman:

🔗 [View Collection in Postman](https://niranjanluitel.postman.co/workspace/Niranjan-Luitel's-Workspace~55337a0f-974a-4dde-8edc-ef133caae7eb/collection/46930916-8988ef69-1f8f-4415-b0b7-7da9f51f6e43?action=share&source=collection_link&creator=46930916)

---

## 📌 Notes

- The database is automatically created on startup.
- Ensure `check_same_thread=False` is set in SQLite for FastAPI compatibility.
- You can later extend this to include delete functionality, pagination, or user authentication.

---

## 🧑‍💻 Author

**Niranjan Luitel**  
📫 [Connect via LinkedIn](https://www.linkedin.com/in/niranjanluitel)  
🔗 [GitHub Profile](https://github.com/niranjanluitel)

---

## 📜 License

This project is licensed under the MIT License.  
See `LICENSE` file for more information.
