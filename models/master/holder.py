from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db_access import Base

class Holder(Base):
    __tablename__ = "holders"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    use = Column(Boolean, default=False)
    disposal = Column(Boolean, default=False)
    blade = relationship("Blade", back_populates="horder")
