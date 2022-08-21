from sqlalchemy.orm import Session

import models
import schemas


def add_new_car(db: Session, car: schemas.Car):

    db_car = models.Car(
        plate_number=car.plate_number, brand=car.brand, model=car.model, name=car.name
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)

    return db_car
