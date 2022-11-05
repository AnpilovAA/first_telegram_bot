from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASE

engine = create_engine(DATABASE)
connect = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
Base.metadata.create_all(engine)
