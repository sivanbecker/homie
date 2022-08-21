import datetime
import sys
from enum import Enum, IntEnum, auto
from typing import List, Optional, Union

import logbook
from pydantic import BaseModel, Field, validator
from pydantic.dataclasses import dataclass
import pendulum

logbook.StreamHandler(sys.stdout).push_application()
_logger = logbook.Logger(__name__)


class Maintainee(str, Enum):
    CAR = "car"
    WASHING_MACHINE = "washing-machine"


class MaintenanceCycle(IntEnum):
    """Maintenance cycle in months"""

    MONTHLY_1 = 1
    MONTHLY_3 = 3
    MONTHLY_6 = 6
    YEARLY_1 = 12
    YEARLY_2 = 24
    YEARLY_3 = 36





class MaintenanceType(BaseModel):
    what: Maintainee = Field(..., title="What is maintained")
    when: MaintenanceCycle = Field(..., title="Specific cycle of maintenance")
    description: str = Field(None, title="Short description of what should be done")

    def __repr__(self):
        return f"<MaintenanceType maintainee: {self.what} / cycle: {self.when} months>"


class Maintenance(BaseModel):

    id: int = Field(..., description="Maintenance record id")
    name: str = Field(..., max_length=64)
    description: str = Field(None, max_length=512)
    start_date: datetime.date = Field(default=None, title="maintenance start date")
    end_date: datetime.date = Field(default=None, title="maintenance end date")
    maintenance_type: MaintenanceType = Field(..., title="The maintenenace type")
    state: MaintenanceState = Field(
        default=MaintenanceState.CREATED, title="Current state of the maintenance"
    )

    def __str__(self) -> str:
        return f"<Maintenance {self.id}: {self.name}>"

    def start(self):
        _logger.debug(f"START MAINTENANCE: {self}")
        assert (
            self.state == MaintenanceState.CREATED
        ), f"Trying to start a maintenance in wrong state {self.state}"
        self.state = MaintenanceState.STARTED
        self.start_date = pendulum.now()

    def done(self):
        _logger.debug(f"COMPLETE MAINTENANCE: {self}")
        assert (
            self.state == MaintenanceState.STARTED
        ), f"Trying to complete maintenance which is not in START state ({self.state})"
        self.state = MaintenanceState.DONE
        self.end_date = pendulum.now()

    def stop(self):
        _logger.debug(f"STOP MAINTENANCE: {self}")
        self.state = MaintenanceState.STOPPED

    def cancel(self):
        _logger.debug(f"CANCEL MAINTENANCE: {self}")
        self.state = MaintenanceState.CANCELED
        self.end_date = pendulum.now()


class Maintainable(BaseModel):
    """for example a car is maintainable since its needs
    maintenance"""

    name: str = Field(..., title="name of maintainable")
    allowed_maintenance_types: List[Union[MaintenanceType, Maintainee]] = Field(
        ..., title="Which maintenance types are allowed for this maintainable"
    )
    maintenance_list: List[Maintenance] = Field(
        [], title="List of completed maintenances"
    )

    def last_maintenance(self) -> Maintenance:
        return self.maintenance_list[-1]

    def next_expected_maintenance(self):
        raise NotImplementedError


CAR_YEARLY_MAINTENANCE_TYPE = MaintenanceType(
    what=Maintainee.CAR,
    when=MaintenanceCycle.YEARLY_1,
    description="Routine yearly car maintenance",
)

CAR_MONTHLY_6_MAINTENANCE_TYPE = MaintenanceType(
    what=Maintainee.CAR,
    when=MaintenanceCycle.MONTHLY_6,
    description="Half year car maintenance",
)
# if __name__ == "__main__":
