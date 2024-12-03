from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db_access import Base

class Line(Base):
    __tablename__ = "lines"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    processing_machines = relationship("ProcessingMachine", back_populates="line")
