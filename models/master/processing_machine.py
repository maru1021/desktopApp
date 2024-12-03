from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_access import Base

class ProcessingMachine(Base):
    __tablename__ = "processing_machines"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    line_id = Column(Integer, ForeignKey("lines.id"), nullable=True)

    line = relationship("Line", back_populates="processing_machines")
