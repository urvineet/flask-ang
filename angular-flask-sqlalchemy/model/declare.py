__author__ = 'Vineet Shivhare'



from sqlalchemy import Column,  String ,Text,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


engine = create_engine('sqlite:///contact_user.db')

Base = declarative_base()

class User(Base):
    """
    User Table
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False,unique=True)


class Contact(Base):
    """"
    Contact table
    """

    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    contact_name = Column(String(250), nullable=False)
    phone = Column(String(20),nullable=False)
    username = Column(String(250), nullable=False)


class Contact_User(Base):
    """
    shared Contact Table
    """
    __tablename__ = 'contact_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    phone = Column(String(250), nullable=False)



Base.metadata.create_all(engine)



