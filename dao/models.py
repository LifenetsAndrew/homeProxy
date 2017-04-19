from dao.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relationship, backref, validates
from flask_restful import fields
import datetime
import bcrypt

class MarshallableModel():

    __type_mapping = {
        int: fields.Integer,
        str: fields.String,
        datetime.datetime: fields.DateTime,
        bool: fields.Boolean,
        list: fields.List,
    }

    __marshallers = {}

    __instance = None

    @classmethod
    def init_marshallers(cls):
        if not MarshallableModel.__instance:
            MarshallableModel.__instance = MarshallableModel()

    def __init__(self):
        mapped = None
        for sub in MarshallableModel.__subclasses__():
            columns = [column for column in inspect(sub).columns]
            mapped = {column.name: MarshallableModel.__type_mapping[column.type.python_type] for column in columns if not column.info.get('skip_marshalling')}
            MarshallableModel.__marshallers[sub] = mapped

            def add_closures(sub,mapped):
                def get_marshaller(self):
                    return mapped
                def get_dict(self):
                    return {name: getattr(self, name, None) for name in mapped.keys()}
                sub.get_marshaller = get_marshaller
                sub.get_dict = get_dict
            add_closures(sub, mapped)



class User(Base, MarshallableModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), unique=True)
    password = Column(String(200), info={'skip_marshalling': True})
    email = Column(String(50), unique=True)

    @validates('password')
    def set_password(self, key, pure_password):
        return bcrypt.hashpw(pure_password.encode('utf-8'), salt=bcrypt.gensalt())

    def check_password(self, pure_password):
        return bcrypt.checkpw(pure_password.encode('utf-8'), self.password.encode('utf-8'))


class Token(Base, MarshallableModel):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True, autoincrement=True, info={'skip_marshalling': True})
    user_id = Column(ForeignKey('user.id'), info={'skip_marshalling': True})
    token = Column(String(50))
    user = relationship('User', backref='tokens')
    sequence_number = Column(Integer)
    expiry = Column(DateTime, info={'skip_marshalling': True})
