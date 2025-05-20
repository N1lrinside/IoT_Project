from sqlalchemy import Column, Integer, Float, Boolean, String, DateTime, ForeignKey
from src.core.database import Base
from datetime import datetime

class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, default=20.0)
    is_open = Column(Boolean, default=False)
    last_temperature_change = Column(DateTime, default=datetime.now())

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    action = Column(String)
    date = Column(DateTime, default=datetime.now())
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)