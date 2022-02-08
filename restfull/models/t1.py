
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class T1(Base):
    __tablename__ = 't1'
    id = Column(Integer,primary_key=True)
    username = Column(String(256))

    def toJson(self):
        """
        :return:
        """
        return json.dumps({'id':self.id,
                           'username':self.username})