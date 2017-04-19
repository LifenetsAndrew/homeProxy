from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import configparser

config = configparser.ConfigParser()
if not len(config.read('home.ini')):
    config['DEFAULT'] = {
        'db': 'mysql+pymysql://root:root@localhost:8889/home',
        'salt': '1234'
    }

engine = create_engine(config['DEFAULT']['db'])
Base = declarative_base(bind=engine)
session = scoped_session(sessionmaker(bind=engine))
Base.query = session.query_property()

def init_db():
    from dao.models import User, Token
    Base.metadata.create_all(engine)
    # u = User()
    # u.login = 'alif'
    # u.password = 'zAEYHmnHT1'
    # add_one(u)



def build_filter(model, filter):
    assert type(filter) == dict
    filtered_query = session.query(model)
    for field, value in filter.items():
        if(hasattr(model, field)):
            filtered_query = filtered_query.filter(getattr(model, field) == value)
    return filtered_query

def find_one(model, filter):
    return build_filter(model, filter).first()

def add_one(obj):
    session.add(obj)
    session.commit()
