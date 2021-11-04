from typing import Optional
import pydantic
from decimal import Decimal

from enum import Enum
from sqlalchemy.orm import backref
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

from pydantic import conint
from datetime import date, datetime

class Sex(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    NOT_KNOWN = 'not known'


class DocumentStatus(str, Enum):
    UNREVIEWED = 'unreviewed'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: pydantic.EmailStr
    hashed_password: str
    birthday: date
    sex: Sex = Field(Sex.NOT_KNOWN)
    createdAt: datetime


class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  

    name: str

    moderated: bool = Field(False) 
    blocked: bool = Field(False)
    # TODO FK NOT NULL MUST BE
    owner_id: Optional[int] = Field(None, foreign_key="businessuser.id")


class CasualUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)    
    balance: Decimal = Field(default=Decimal(0))

    #FK
    account_id: Optional[int] = Field(default=None, foreign_key="user.id")
    account: User = Relationship()


class BusinessUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)    

    #FK
    account_id: Optional[int] = Field(default=None, foreign_key="user.id")
    account: User = Relationship()


class DocumentType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  
    name: str


class CompanyDocument(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 

    content: str
    status: DocumentStatus = Field(DocumentStatus.UNREVIEWED)
    company_id: int = Field(foreign_key='company.id')
    company: Company = Relationship()


class VehicleCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str


class Vehicle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 

    vehicle_gos_nomer: str
    passenger_count: int

    category_id: int = Field(foreign_key="vehiclecategory.id")
    category: VehicleCategory = Relationship()

    company_id: int = Field(foreign_key="company.id")
    company: Company = Relationship()



engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)




