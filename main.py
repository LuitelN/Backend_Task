from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

# Database setup
DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ORM Models
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    blog = relationship("Blog", back_populates="category", uselist=False)

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))  # remove unique=True
    category = relationship("Category", back_populates="blog")

# Pydantic Schemas
class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class BlogBase(BaseModel):
    title: str
    description: str
    category_name: str

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    pass

class BlogSchema(BlogBase):
    id: int
    category: CategorySchema

    class Config:
        from_attributes = True


# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI instance
app = FastAPI()

# Initialize database
init_db()

# Endpoints
@app.get("/blogs", response_model=list[BlogSchema])
def get_all_blogs(db: Session = Depends(get_db)):
    return db.query(Blog).all()

@app.get("/blogs/{blog_id}", response_model=BlogSchema)
def get_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.post("/blogs", response_model=BlogSchema, status_code=201)
def create_blog(blog_in: BlogCreate, db: Session = Depends(get_db)):
    # Check if category exists or create
    category = db.query(Category).filter(Category.name == blog_in.category_name).first()
    if category is None:
        category = Category(name=blog_in.category_name)
        db.add(category)
        db.commit()
        db.refresh(category)
    # Create blog
    new_blog = Blog(
        title=blog_in.title,
        description=blog_in.description,
        category_id=category.id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.put("/blogs/{blog_id}", response_model=BlogSchema)
def update_blog(blog_id: int, blog_in: BlogUpdate, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    # Update category if changed
    if blog.category.name != blog_in.category_name:
        category = db.query(Category).filter(Category.name == blog_in.category_name).first()
        if category is None:
            category = Category(name=blog_in.category_name)
            db.add(category)
            db.commit()
            db.refresh(category)
        blog.category_id = category.id
    # Update other fields
    blog.title = blog_in.title
    blog.description = blog_in.description
    db.commit()
    db.refresh(blog)
    return blog