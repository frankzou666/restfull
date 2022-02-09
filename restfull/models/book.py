
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    year = Column(Integer)

    def toJson(self):
        """
        :return:
        """
        return json.dumps({'id': self.id,
                           'title': self.title,
                           'year': self.year})