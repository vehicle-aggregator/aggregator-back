from typing import List
from fastapi import FastAPI, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body

from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, StatementError
import pydantic 

from auth import get_business_user, get_current_active_user
from model import Company, CompanyWrite, User, UserIn, UserOut, engine, Vehicle, get_session

app =  FastAPI()

@app.post("/create", response_model=Company)
def create_company(
    session: Session = Depends(get_session),
    user: User = Depends(get_business_user),
    company_in: CompanyWrite = Body(...)
):
    company = Company(name=company_in.name)
    company.owner_id = user.id
    session.add(company)
    session.commit()
    session.refresh(company)
    return company


@app.get("/list", response_model=List[Company])
def company_list(
    session: Session = Depends(get_session)
):
    return session.exec(select(Company)).all()