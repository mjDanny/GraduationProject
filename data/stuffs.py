import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Stuffs(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Stuffs'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String,
                              nullable=False)
    pic = sqlalchemy.Column(sqlalchemy.String,
                            nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer,
                              nullable=False)
    # Привяжем таблицу материалов к пользователям (Создаём внешний ключ)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("Users.id"))
    user = orm.relationship("User")

    def __repr__(self):
        return f"<Stuffs id={self.id} title='{self.title}'>"

    def get_title(self):
        return self.title
