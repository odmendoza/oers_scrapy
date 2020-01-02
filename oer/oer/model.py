from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:@localhost/oerintegrationdb', echo=True)
Base = declarative_base(engine)


class Triple(Base):
    __tablename__ = 'triple'
    __table_args__ = {'autoload': True}


def load_session():
    """"""

    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
