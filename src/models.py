import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er


Base = declarative_base()

# Tabla de asociación para la relación de muchos a muchos entre usuarios y seguidores
followers_association = Table('followers', Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id')),
    Column('followed_id', Integer, ForeignKey('users.id'))
)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    usersname = Column(String(30), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(128))
    name = Column(String(50))
    bio = Column(Text())
    profile_picture_url = Column(String(255))
    followed = relationship(
        'Users', secondary=followers_association,
        primaryjoin=(followers_association.c.follower_id == id),
        secondaryjoin=(followers_association.c.followed_id == id),
        backref='followers'
    )
    
    posts = relationship('Post', backref='author')
    comments = relationship('comments', backref='author')
    likes = relationship('likes', backref='users')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id'))
    caption = Column(Text())
    image_url = Column(String(255), nullable=False)
    
    comments = relationship('comments', backref='post')
    likes = relationship('likes', backref='post')

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    text = Column(Text(), nullable=False)

class Likes(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
