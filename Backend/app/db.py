from sqlalchemy import Column, String, Integer, Boolean, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DATABASE_URL = "sqlite:///./database/database.db"
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    author = Column(String)
    genre = Column(String)
    stock = Column(Integer)
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    status = Column(Boolean)
    role = Column(String)

    borrow = relationship("Borrow", back_populates="user_borrow")
    devices = relationship("Device", back_populates="user")
    

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    device_id = Column(String)
    user = relationship(
        "User",
        back_populates="devices"
    )

class Borrow(Base):
    __tablename__ = "borrow"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)

    user_borrow = relationship("User", back_populates="borrow")
    
class Verification_Pending(Base):
    __tablename__ = "verification"
    
    id = Column(Integer, primary_key=True)
    user_email = Column(String)
    otp = Column(String)
    new_device_id = Column(String)
    expires_at = Column(String)
    
Base.metadata.create_all(engine)