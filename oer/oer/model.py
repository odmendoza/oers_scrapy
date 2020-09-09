from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://scrapy:pwdScrapy!3@localhost/oersdb', echo=True)
Base = declarative_base(engine)


class Triple(Base):
    __tablename__ = 'crawl'
    __table_args__ = {'autoload': True}


def load_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
