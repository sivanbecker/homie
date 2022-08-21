from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
import models
import schemas
from fastapi import HTTPException

# Utility functions for :
# 1. Reading all Maintainees
# 2. Reading all maintenances


def read_maintenances(db: Session):
    return db.query(models.Maintenance).all()

def read_maintainees(db: Session):
    return db.query(models.Maintainee).all()

# Utility functions for :
# 1. Creating a Maintainee
# 2. Creating a maintenance

def create_maintainee(db: Session, maintainee: schemas.MaintaineeCreate):
    db_maintainee = models.Maintainee(**maintainee.dict(), )
    db.add(db_maintainee)
    db.commit()
    db.refresh(db_maintainee)
    return db_maintainee

def create_maintenance(db: Session, maintenance: schemas.MaintenanceCreate, maintainee_id: int):
    try:
        db.query(models.Maintainee).filter(models.Maintainee.id == maintainee_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Maintainee id {maintainee_id} not in DB")
    db_maintenance = models.Maintenance(**maintenance.dict(), maintainee_id=maintainee_id)
    db.add(db_maintenance)
    db.committer()
    db.refresh(db_maintenance)
    return db_maintenance