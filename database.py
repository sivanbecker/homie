from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
from fastapi import HTTPException
from functools import partial

# TODO : take this from env variable
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://localhost/home"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    db.committer = partial(sqlite_commit_with_err_handling, db) if 'sqlite' in db.bind.url else partial(db.commit)
    try:
        yield db
    finally:
        db.close()

def sqlite_commit_with_err_handling(db: Session):
    try:
        db.commit()
    except OperationalError as exc:
        if 'database is locked' in str(exc):
            raise HTTPException(status_code=500, detail=str(exc))