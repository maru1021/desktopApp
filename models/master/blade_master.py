from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_access import Base

class BladeMaster(Base):
    __tablename__ = "blade_masters"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    horder_master_id = Column(Integer, ForeignKey("horder_masters.id"), nullable=True)
    blade_classification_id = Column(Integer, ForeignKey("blade_classifications.id"), nullable=False)

    blade_classification = relationship("BladeClassification", back_populates="blade_master")
    horder_master = relationship("HorderMaster", back_populates="blade_master")
    blades = relationship("Blade", back_populates="blade_master")
