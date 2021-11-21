from fastapi import FastAPI, Depends, status
from fastapi.exceptions import HTTPException

from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
import pydantic 

from auth import get_current_active_user
from model import User, UserIn, UserOut, engine, Vehicle

app =  FastAPI()

@app.post('/create', response_model=Vehicle,
#  dependencies=[Depends(get_current_active_user)]
)
def create(vehicle: Vehicle):
    with Session(engine) as session:
        session.add(vehicle)
        session.commit()
        session.refresh(vehicle)
        return vehicle