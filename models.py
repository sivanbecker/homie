from enum import IntEnum
from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, Date, Enum, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null

from database import Base

# class Car(Base):
#     __tablename__ = "cars"

#     id = Column(Integer, primary_key=True, index=True)
#     plate_number = Column(String, unique=True, index=True)
#     name = Column(String)
#     brand = Column(String)
#     model = Column(String)


class MaintaineeType(PyEnum):
    CAR = "Car"
    WASHING_MACHINE = "Washing-Machine"
    REFRIGERATOR = "Refrigerator"
    ELECTRIC_BICYCLE = "Electric-Bicycle"


class MaintenanceState(IntEnum):
    CREATED = 1
    STARTED = 2
    DONE = 3
    STOPPED = 4
    CANCELED = 5


class Maintainee(Base):
    __tablename__ = "maintainee"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mtype = Column(Enum(MaintaineeType))  # maintainee type
    maintenances = relationship("Maintenance", back_populates="maintainee")


class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    state = Column(Enum(MaintenanceState))
    maintainee_id = Column(Integer, ForeignKey("maintainee.id"))
    maintainee = relationship("Maintainee", back_populates="maintenances")
