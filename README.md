#  Blog API with FastAPI

A simple and scalable RESTful API for managing blog posts and categories built with **FastAPI**, **SQLAlchemy**, and **SQLite**. This API supports creating, reading, and updating blog posts with category management. 
The main.py file contains the API for managing blog posts and Ques2.py consists of 2nd Question of the assignment. 

---

##  Features

- Create and update blog posts with category handling  
- Auto-create categories if they don’t exist  
- Retrieve all blogs or a single blog by ID  
- SQLite database 
- Pydantic models for request validation and response schema
- SQLAlchemy ORM for database interaction
- Postman Collection included for easy testing

---

##  Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework  
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit and ORM  
- [SQLite](https://www.sqlite.org/) - Lightweight relational DB (used for local development)  
- [Pydantic](https://docs.pydantic.dev/) - Data validation and settings management

---

##  Getting Started

### 1. **Clone the repository**
```bash
git clone https://github.com/LuitelN/Backend_Task

```

### 2. **Create a virtual environment and activate it**

### 3. **Install dependencies**
```bash
pip install fastapi, uvicorn, sqlalchemy, pydantic

```

### 4. **Run the application**
```bash
uvicorn main:app --reload
```

The API will be live at:  
`http://127.0.0.1:8000`

---

## API Endpoints

###  Get All Blogs  
`GET http://127.0.0.1:8000/blogs
`  
Returns a list of all blogs.

### Get Blog by ID  
`GET http://127.0.0.1:8000/blogs/1`  
Returns a specific blog with its category.

### Create Blog  
`POST http://127.0.0.1:8000/blogs
`  
Creates a blog. If the category does not exist, it is automatically created.

**Sample Body**
```json
{
  "title": "My First Blog",
  "description": "This is a test blog.",
  "category_name": "Tech"
}
```

### Update Blog  
`PUT http://127.0.0.1:8000/blogs/1`  
Updates a blog and reassigns a category if needed.

---

## Database Models

### Blog
- `id`: int
- `title`: str
- `description`: str
- `category_id`: int

### Category
- `id`: int
- `name`: str

---

## Postman Collection

You can test the API using Postman:

[View Collection in Postman](https://niranjanluitel.postman.co/workspace/Niranjan-Luitel's-Workspace~55337a0f-974a-4dde-8edc-ef133caae7eb/collection/46930916-8988ef69-1f8f-4415-b0b7-7da9f51f6e43?action=share&source=collection_link&creator=46930916)

---

## Author

**Niranjan Luitel**  
 [GitHub Profile](https://github.com/LuitelN)

---
