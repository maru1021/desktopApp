from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db_access import Base

class Blade(Base):
    __tablename__ = "blades"
    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    process = Column(String)
    disposal = Column(Boolean, default=False)
    blade_master_id = Column(Integer, ForeignKey("blade_masters.id"), nullable=False)
    horder_id = Column(Integer, ForeignKey("horders.id"), nullable=True)

    blade_master = relationship("BladeMaster", back_populates="blade")
    horder = relationship("Horder", back_populates="blade")
