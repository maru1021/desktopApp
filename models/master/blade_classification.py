from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db_access import Base

class BladeClassification(Base):
    __tablename__ = "blade_classifications"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    blade = relationship("Horde", back_populates="blade_classification")
