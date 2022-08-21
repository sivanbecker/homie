from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.class_validators import validator

from models import MaintenanceState, MaintaineeType
from models import Maintainee as MaintaineeModel


class MaintenanceBase(BaseModel):

    name: str = Field(..., title="Name describing the maintenance")
    start_date: date = Field(default=None, title="When did the maintenance start")
    end_date: date = Field(default=None, title="When did the maintenance end")
    state: MaintenanceState = Field(
        default=MaintenanceState.CREATED, title="One of maintenance states"
    )


class MaintaineeBase(BaseModel):
    name: str = Field(..., title="Name describing the maintainee")
    mtype: MaintaineeType = Field(..., title="What is the maintainee type")


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintaineeCreate(MaintaineeBase):
    pass


class Maintenance(MaintenanceBase):
    id: int
    maintainee_id: int

    class Config:
        orm_mode = True


class Maintainee(MaintaineeBase):
    id: int

    class Config:
        orm_mode = True
