from typing import List, Literal
from fastapi import FastAPI, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body

from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
import pydantic 

from auth import get_business_user, get_current_active_user
from model import BusinessUser, Company, User, UserIn, UserOut, VehicleCategory, VehicleWrite, engine, Vehicle, get_session

app =  FastAPI()

with Session(engine) as session:
    stat = select(VehicleCategory)
    res = session.exec(stat).all()
    category_names = tuple(c.name for c in res)

@app.post('/create', response_model=Vehicle)
def create(
    session: Session = Depends(get_session),
    user: User = Depends(get_business_user),
    vehicle_in: VehicleWrite = Body(...),
    vehicle_category: Literal[category_names] = Body(...) # type: ignore
):
    category = session.exec(select(VehicleCategory).where(VehicleCategory.name == vehicle_category)).one()
    account = session.exec(select(BusinessUser).where(BusinessUser.account_id == user.id)).one()
    company = session.exec(select(Company).where(Company.owner_id == account.id)).one()
    vehicle = Vehicle(
        category_id=category.id,
        company_id=company.id,
        **vehicle_in.dict()
    )
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle


@app.get("/list", response_model=List[Vehicle])
def vehicle_list(session: Session = Depends(get_session)):
    return session.exec(select(Vehicle)).all()

