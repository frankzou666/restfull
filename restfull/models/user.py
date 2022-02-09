
from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import pbkdf2_sha256 as sha256
import json
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(512))
    password = Column(String(512))
    created = Column(DateTime)

    def toJson(self):
        """
        :return:
        """
        return json.dumps({'id': self.id,
                           'username': self.username,
                           'created': self.created.strftime('%Y-%m-%d %H:%M')})

    @staticmethod
    def generatePassword(password):
        return sha256.hash(password)

    @staticmethod
    def verifyPassword(password, hashstr):
        return sha256.verify(password, hashstr)