from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative models
Base = declarative_base()

#class for users, used for registration and login
class User(Base):
    __tablename__ = 'user'

    name = Column(String(32), primary_key=True, nullable=False)
    password = Column(String(512))
#class for students, used for storing student information
class Student(Base):
    __tablename__ = 'student'

    id = Column(String(9), primary_key=True, unique=True)
    name = Column(String(32), nullable=False)
    age = Column(Integer)
    gender = Column(String(1))
    major = Column(String(32))
    phone = Column(String(32))
#class for scores, used for storing student scores
class Score(Base):
    __tablename__ = 'score'

    id = Column(String(9), primary_key=True, unique=True)
    name = Column(String(32), nullable=False)
    CS1030 = Column(Integer)
    CS1100 = Column(Integer)
    CS2030 = Column(Integer)
#class for absences, used for storing student absences
class Absence(Base):
    __tablename__ = 'absence'

    id = Column(String(9), primary_key=True)
    name = Column(String(32), nullable=False)
    absences = Column(Integer)

engine = create_engine('sqlite:///students.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)