import sqlalchemy

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'Users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String,
                             nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True,
                              unique=True,
                              nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String,
                                        nullable=True)
    stuffs = orm.relationship("Stuffs", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
