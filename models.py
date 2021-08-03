from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, index=True)
    name = Column(String)
    brand = Column(String)
    model = Column(String)

