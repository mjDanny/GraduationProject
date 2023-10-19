import sqlalchemy
from .db_session import SqlAlchemyBase


class Zip(SqlAlchemyBase):
    __tablename__ = 'Zips'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    path = sqlalchemy.Column(sqlalchemy.String(200), nullable=False)

    def __repr__(self):
        return f"Zips('{self.name}', '{self.path}')"
