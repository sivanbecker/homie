from enum import Enum
from typing import List, Optional, Union

import logbook
from pydantic import BaseModel, Field, main, validator

from data_classes.maintenance import (
    CAR_YEARLY_MAINTENANCE_TYPE,
    CAR_MONTHLY_6_MAINTENANCE_TYPE,
    Maintainable,
    Maintenance,
    Maintainee,
    MaintenanceType,
)

_logger = logbook.Logger(__name__)


class CarBrand(str, Enum):
    kia = "Kia"


class CarModel(str, Enum):
    forte = "Forte"


class Car(Maintainable):
    id: Optional[int]
    plate_number: str = Field(
        ..., description="Car plate number", max_length=10, min_length=9
    )
    brand: Optional[CarBrand] = Field(..., title="The Car's Brand")
    model: Optional[CarModel] = Field(..., title="The Car's Model")
    allowed_maintenance_types: List[Union[MaintenanceType, Maintainee]] = Field(
        default=Maintainee.CAR, title="Which maintenance types are allowed for this maintainable"
    )

    class Config:
        orm_mode = True
        
    def __str__(self):
        return f"<CAR: {self.name}:{self.plate_number}>"

    @validator("plate_number")
    def validate_7_or_8_plate_number(cls, v):
        try:
            int(v.replace("-", ""))
        except ValueError:
            raise ValueError(f"Non valid car number {v}")
        return v

    def add_maintenance(self, maintenance: Maintenance):
        _logger.debug(f"Add new maintenance to {self}")
        assert (
            maintenance.maintenance_type.what in self.allowed_maintenance_types
        ), f"Maintenance {maintenance} is not in allowed types -> {self.allowed_maintenance_types}"
        self.maintenance_list.append(maintenance)


if __name__ == "__main__":
    kia_forte = Car(
        id=1,
        name="Kia Forte",
        allowed_maintenance_types=[Maintainee.CAR],
        plate_number="111-11-111",
        brand=CarBrand.kia,
        model=CarModel.forte,
    )
    CAR_YEARLY_MAINTENANCE = Maintenance(
        id=1, name="Kia Forte 2021", maintenance_type=CAR_YEARLY_MAINTENANCE_TYPE
    )
    CAR_MOTHLY_6_MAINTENANCE = Maintenance(
        id=2, name="Kia Forte 2021 (6 months)", maintenance_type=CAR_MONTHLY_6_MAINTENANCE_TYPE
    )

    kia_forte.add_maintenance(CAR_YEARLY_MAINTENANCE)
    kia_forte.last_maintenance().start()
    kia_forte.last_maintenance().stop()
    kia_forte.add_maintenance(CAR_MOTHLY_6_MAINTENANCE)
    kia_forte.last_maintenance().start()
    kia_forte.last_maintenance().done()
