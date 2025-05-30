# Initialize database package
from .models import Base
from .operations import SchoolOperations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def init_db():
    engine = create_engine('sqlite:///school.db')
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()