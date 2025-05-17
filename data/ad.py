import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Ad(SqlAlchemyBase):
    __tablename__ = 'ad'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    creator_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    design = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    floor = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    purpose = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    square = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    state = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.date(1, 1, 1))
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
