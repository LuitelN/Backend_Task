from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session


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
    blogs = relationship("Blog", back_populates="category")


class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="blogs")



# Pydantic Schemas
class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BlogBase(BaseModel):
    title: str
    description: str


class BlogCreate(BlogBase):
    category_name: str


class BlogUpdate(BlogBase):
    category_name: str


class BlogSchema(BlogBase):
    id: int
    category: CategorySchema

    class Config:
        orm_mode = True



# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# FastAPI App

app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)



# Routes

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
    category = db.query(Category).filter(Category.name == blog_in.category_name).first()
    if not category:
        category = Category(name=blog_in.category_name)
        db.add(category)
        db.commit()
        db.refresh(category)
    blog = Blog(
        title=blog_in.title,
        description=blog_in.description,
        category_id=category.id,
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@app.put("/blogs/{blog_id}", response_model=BlogSchema)
def update_blog(blog_id: int, blog_in: BlogUpdate, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if blog.category.name != blog_in.category_name:
        category = db.query(Category).filter(Category.name == blog_in.category_name).first()
        if not category:
            category = Category(name=blog_in.category_name)
            db.add(category)
            db.commit()
            db.refresh(category)
        blog.category_id = category.id

    blog.title = blog_in.title
    blog.description = blog_in.description
    db.commit()
    db.refresh(blog)
    return blog
