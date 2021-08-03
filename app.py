from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
import crud, models, schemas
from database import get_db, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()



@app.post("/cars/", response_model=schemas.Car)
def create_car(car: schemas.Car, db: Session = Depends(get_db)):
    return crud.add_new_car(db=db, car=car)


