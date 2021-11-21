from typing import List, Optional
from uuid import UUID, uuid4
from decimal import Decimal
from datetime import date, datetime

from enum import Enum
from sqlalchemy.orm import backref
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

import pydantic
from pydantic import conint, conlist, BaseModel


class Sex(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    NOT_KNOWN = 'not known'


class DocumentStatus(str, Enum):
    UNREVIEWED = 'unreviewed'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class UserBase(BaseModel):
    email: pydantic.EmailStr
    birthday: date
    sex: Sex = Field(Sex.NOT_KNOWN)

class User(SQLModel, UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    createdAt: datetime = Field(default_factory=datetime.now)
    token: UUID = Field(default_factory=uuid4)
    disabled: bool = Field(default=False)


class UserOut(UserBase):
    ...


class UserIn(UserBase):

    password: str


class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  

    name: str

    moderated: bool = Field(False) 
    blocked: bool = Field(False)
    # TODO FK NOT NULL MUST BE
    owner_id: Optional[int] = Field(None, foreign_key="businessuser.id")


class CompanyWrite(BaseModel):
    name: str


class Account(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)   

    account_id: Optional[int] = Field(default=None, foreign_key="user.id")
    # account: User = Relationship(link_model=User)
    

class CasualUser(Account, SQLModel, table=True):
    balance: Decimal = Field(default=Decimal(0))


class BusinessUser(Account, SQLModel,  table=True):
    """BusinessUser"""


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


class VehicleWrite(BaseModel):

    vehicle_gos_nomer: str
    passenger_count: int

class Place(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 

    name: str
    description: str
    country: str
    longitude: float
    latitude: float


class Route(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 

    from_place_id: int = Field(foreign_key="place.id")
    to_place_id: int = Field(foreign_key="place.id")

    to_place: Place = Relationship(sa_relationship_kwargs={'foreign_keys': "[Route.to_place_id]"})
    from_place: Place = Relationship(sa_relationship_kwargs={'foreign_keys': "[Route.from_place_id]"})


class TripStatus(str, Enum):
    DONE = 'done'
    CANCELED = 'cancel'
    ANTICIPATED = 'anticipated'


class Trip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    description: str
    start_at: datetime 
    end_at: datetime 
    status: TripStatus = Field(TripStatus.ANTICIPATED)

    route_id: int = Field(foreign_key="route.id")
    route: Route = Relationship()

    vehicle_id: int = Field(foreign_key="vehicle.id")
    vehicle: Vehicle = Relationship()


class Passenger(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    first_name: str
    last_name: str
    middle_name: str
    birthday: date
    document_detail: str


    owner_id: int = Field(foreign_key="casualuser.id")
    owner: CasualUser = Relationship()

    document_type_id: int = Field(foreign_key="documenttype.id")
    document_type: DocumentType = Relationship()


class TicketCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    ratio: float


class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    price: Decimal 
    created_at: datetime

    trip_id: int = Field(foreign_key='trip.id')
    category_id: int = Field(foreign_key='ticketcategory.id')
    passenger_id: int = Field(foreign_key='passenger.id')

    trip: Trip = Relationship()
    category: TicketCategory = Relationship()
    passenger: Passenger = Relationship()
    

class Moderator(Account, SQLModel, table=True):
    """Moderator"""


class CompanyApprovementStatus(str, Enum):
    UNREVIEWED = 'unreviewed'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class CompanyApprovement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  

    status: CompanyApprovementStatus = Field(CompanyApprovementStatus.UNREVIEWED)
    status_changed: datetime 

    company_id: int = Field(foreign_key="company.id")
    approved_by_id: int = Field(foreign_key="moderator.id")

    company: Company = Relationship()
    approved_by: Moderator = Relationship()


engine = create_engine("sqlite:///database.db?check_same_thread=False")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


