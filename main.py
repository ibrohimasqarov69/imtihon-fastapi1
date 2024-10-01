from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import Base, NewsPost, Comment, Favorite
from .crud import add_comment, get_comments, save_favorite, get_favorites
from .auth import get_current_user
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from .models import Base, NewsPost, Comment, Favorite
from .crud import add_comment, get_comments, save_favorite, get_favorites
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    category: str
    preview_image: str
    description: str
    images: List[str]

# Sample data
posts = [
    Post(
        title="Exciting Event This Month!",
        category="Events",
        preview_image="preview1.jpg",
        description="Catch up on this month’s most exciting event highlights.",
        images=["full1.jpg", "full2.jpg", "full3.jpg"]
    ),
    Post(
        title="New Product Launch",
        category="Announcements",
        preview_image="preview2.jpg",
        description="Discover the latest products we've launched.",
        images=["product1.jpg", "product2.jpg", "product3.jpg"]
    ),
    # Add more posts as needed
]

@app.get("/posts")
def get_posts():
    return posts

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    if 0 <= post_id < len(posts):
        return posts[post_id]
    return {"error": "Post not found"}



DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/news/{news_post_id}/comment/")
def create_comment(news_post_id: int, content: str, db: Session = Depends(get_db)):
    return add_comment(db, news_post_id, content)

@app.get("/news/{news_post_id}/comments/")
def read_comments(news_post_id: int, db: Session = Depends(get_db)):
    return get_comments(db, news_post_id)

@app.post("/news/{news_post_id}/favorite/")
def create_favorite(news_post_id: int, db: Session = Depends(get_db)):
    return save_favorite(db, news_post_id)

@app.get("/news/{news_post_id}/favorites/")
def read_favorites(news_post_id: int, db: Session = Depends(get_db)):
    return get_favorites(db, news_post_id)




app = FastAPI()

# Database setup (same as before)
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/news/{news_post_id}/")
def read_news(news_post_id: int, db: Session = Depends(get_db)):
    news_post = db.query(NewsPost).filter(NewsPost.id == news_post_id).first()
    if news_post is None:
        raise HTTPException(status_code=404, detail="News post not found")
    return news_post

@app.post("/news/{news_post_id}/comment/")
def create_comment(news_post_id: int, content: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return add_comment(db, news_post_id, content)

@app.get("/news/{news_post_id}/comments/")
def read_comments(news_post_id: int, db: Session = Depends(get_db)):
    return get_comments(db, news_post_id)

@app.post("/news/{news_post_id}/favorite/")
def create_favorite(news_post_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return save_favorite(db, news_post_id)

@app.get("/news/{news_post_id}/favorites/")
def read_favorites(news_post_id: int, db: Session = Depends(get_db)):
    return get_favorites(db, news_post_id)
