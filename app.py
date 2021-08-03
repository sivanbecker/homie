import sys
from typing import List, Optional

import logbook
from sqlalchemy.orm.session import Session

import crud
import models
import schemas
from database import engine, get_db
from fastapi import FastAPI, Query
from fastapi.param_functions import Depends
from sentry import init_sentry

logbook.StreamHandler(sys.stdout).push_application()
_logger = logbook.Logger(__name__)

init_sentry()

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.post("/cars/", response_model=schemas.Car)
def create_car(car: schemas.Car, db: Session = Depends(get_db)):
    return crud.add_new_car(db=db, car=car)
