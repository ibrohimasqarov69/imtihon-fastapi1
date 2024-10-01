from sqlalchemy.orm import Session
from .models import NewsPost, Comment, Favorite

def add_comment(db: Session, news_post_id: int, content: str):
    comment = Comment(content=content, news_post_id=news_post_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_comments(db: Session, news_post_id: int):
    return db.query(Comment).filter(Comment.news_post_id == news_post_id).all()

def save_favorite(db: Session, news_post_id: int):
    favorite = Favorite(news_post_id=news_post_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite

def get_favorites(db: Session, news_post_id: int):
    return db.query(Favorite).filter(Favorite.news_post_id == news_post_id).all()
