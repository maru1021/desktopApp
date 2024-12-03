from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db_access import Base

class HolderMaster(Base):
    __tablename__ = "holder_masters"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    blade_master = relationship("BladeMaster", back_populates="horder_master")
