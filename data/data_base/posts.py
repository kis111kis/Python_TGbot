import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'posts'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    year = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    month = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    day = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hour = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    minute = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    theme = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='No_theme')
    created_by = sqlalchemy.Column(sqlalchemy.String, nullable=True)
