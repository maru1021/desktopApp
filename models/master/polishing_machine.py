from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db_access import Base

class PolishingMachine(Base):
    __tablename__ = "polishing_machines"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
