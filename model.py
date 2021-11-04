from typing import Optional
import pydantic
from decimal import Decimal

from enum import Enum
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

from pydantic import conint
from datetime import date, datetime

class Sex(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    UNDEFINED = 'undefined'


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: pydantic.EmailStr
    hashed_password: str
    birthday: date
    sex: Sex = Field(Sex.UNDEFINED)
    createdAt: datetime


class CasualUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)    
    balance: Decimal = Field(default=Decimal(0))

    #FK
    account_id: Optional[int] = Field(default=None, foreign_key="user.id")
    account: User = Relationship(back_populates='casual_users')




engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)




