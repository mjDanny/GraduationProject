import sqlalchemy
from .db_session import SqlAlchemyBase


class Image(SqlAlchemyBase):
    __tablename__ = 'Files'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    path = sqlalchemy.Column(sqlalchemy.String(200), nullable=False)

    def __repr__(self):
        return f"Image('{self.name}', '{self.path}')"
