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

models.Base.metadata.create_all(bind=engine) # Create tables in DB


app = FastAPI()

@app.get("/maintenances/",response_model=List[schemas.Maintenance])
def get_maintenances(db: Session = Depends(get_db)):
    return crud.read_maintenances(db)

@app.get("/maintainees/",response_model=List[schemas.Maintainee])
def get_maintainees(db: Session = Depends(get_db)):
    return crud.read_maintainees(db)

@app.post("/maintainees/", response_model=schemas.Maintainee)
def add_maintainee(maintainee: schemas.MaintaineeCreate, db: Session = Depends(get_db)):
    return crud.create_maintainee(db=db, maintainee=maintainee)

@app.post("/maintainees/{maintainee_id}/maintenance/", response_model=schemas.Maintenance)
def add_maintenance(maintenance: schemas.MaintenanceCreate, maintainee_id: int, db: Session = Depends(get_db)):
    return crud.create_maintenance(db=db, maintenance=maintenance, maintainee_id=maintainee_id)