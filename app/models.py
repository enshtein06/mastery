from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class User(Base):
  __tablename__ = "users"

  id =  Column(Integer, primary_key=True, nullable=False)
  email = Column(String, unique=True)
  password = Column(String)
  vendor_id = Column(String, unique=True)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text("now()"))

class Activity(Base):
  __tablename__ = "activities"

  id = Column(Integer, primary_key=True, nullable=False)
  title = Column(String, nullable=False)
  type = Column(String)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text("now()"))
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

  # User here refers to User sqlalchemy class
  user = relationship("User")

class ExperienceBlock(Base):
  __tablename__ = "experience_blocks"

  id = Column(Integer, primary_key=True, nullable=False)
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
  activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"))
  time_in_seconds = Column(Integer, nullable=False)
  description = Column(String)
  to_improve = Column(String)
  rating = Column(Integer)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text("now()"))
