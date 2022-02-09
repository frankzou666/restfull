
from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.ext.declarative import declarative_base
import json
import datetime

Base = declarative_base()


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    created = Column(DateTime)

    def toJson(self):
        """
        :return:
        """
        return json.dumps({'id': self.id,
                           'first_name': self.first_name,
                           'last_name': self.last_name,
                           'created': self.created.strftime('%Y-%m-%d %H:%M')})