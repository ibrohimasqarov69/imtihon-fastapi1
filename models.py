from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NewsPost(Base):
    __tablename__ = 'news_posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)

    comments = relationship('Comment', back_populates='news_post')
    favorites = relationship('Favorite', back_populates='news_post')

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    news_post_id = Column(Integer, ForeignKey('news_posts.id'))

    news_post = relationship('NewsPost', back_populates='comments')

class Favorite(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True, index=True)
    news_post_id = Column(Integer, ForeignKey('news_posts.id'))

    news_post = relationship('NewsPost', back_populates='favorites')
