from sqlalchemy import Integer, Column, String

from src.database import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    message = Column(String)