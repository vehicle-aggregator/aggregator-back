"""
Модуль для создания данных-заглушки
"""

import random
from uuid import uuid4
import os
from datetime import date, datetime

from sqlmodel import create_engine, Session

from mimesis import Person, Datetime, Internet, Food, Address
from mimesis.locales import Locale
from mimesis.enums import Gender

from model import (BusinessUser, CasualUser, Company, CompanyDocument, DocumentStatus,
                     DocumentType, Place, Route, Sex, User, Vehicle, VehicleCategory)


fake_person = Person(locale=Locale.RU)
fake_dt = Datetime()
fake_internet = Internet()
fake_food = Food()
fake_address = Address()

N_USERS = 100
N_CASUAL_USERS = 30
N_BUSINESS_USERS = 30
N_COMPANIES = 30
N_COMPANY_DOCUMENTS = 60
N_VEHICLES = 20
N_PLACES = 20
N_ROUTES = 20

SQLITE_DB = "database.db"




engine = create_engine(f'sqlite:///{SQLITE_DB}')



with Session(engine) as session:
    for _ in range(N_USERS):
        session.add(
            User(
                email=fake_person.email(unique=True),
                sex=random.choice(list(Sex)),
                createdAt=fake_dt.datetime(start=2020),
                hashed_password=uuid4().hex,
                birthday=fake_dt.date(start=1917)
            )
        )
    session.commit()

    for _ in range(N_CASUAL_USERS):
        session.add(
            CasualUser(
                balance=f'{random.randint(0, 10000)}{random.randint(0, 99)}',
                account_id=random.randint(1, N_USERS)
            )
        )

    session.commit()

    for _ in range(N_BUSINESS_USERS):
        session.add(
            BusinessUser(account_id=random.randint(1, N_USERS))
        )
    session.commit()

    for _ in range(N_COMPANIES):
        session.add(
            Company(
                name=f'ООО "{fake_food.fruit()}"',
                owner_id=random.randint(1, N_BUSINESS_USERS)
            )
        )    
    session.commit()

    session.add(DocumentType(name="паспорт РФ"))
    session.add(DocumentType(name="Лицензия ТК"))
    session.add(DocumentType(name="Свидетельство о рождение"))
    session.add(DocumentType(name="Справка о том, что не верблюд"))
    session.commit()

    for _ in range(N_COMPANY_DOCUMENTS):
        session.add(
            CompanyDocument(
                content=uuid4().hex,
                status=random.choice(list(DocumentStatus)),
                company_id=random.randint(1, N_COMPANIES)
            ) 
            
        )
    session.commit()


    session.add(VehicleCategory(name="микроавтобус"))
    session.add(VehicleCategory(name="автобус"))
    session.add(VehicleCategory(name="туристический автобус"))
    session.add(VehicleCategory(name="патибас"))
    session.commit()

    for _ in range(N_VEHICLES):
        session.add(
            Vehicle(
                vehicle_gos_nomer=f"{random.choice(['аа', 'ао', 'оо'])}{random.randint(100, 999)}{random.choice('абмву')}{random.randint(1, 99)}",
                passenger_count=random.randint(8, 45),
                category_id=random.randint(1, 4),
                company_id=random.randint(1, N_COMPANIES)
            )
        )
    session.commit()


    for _ in range(N_PLACES):
        session.add(
            Place(
                name=fake_address.city(),
                description=f"{fake_address.continent()} {fake_address.country()} {fake_address.federal_subject()}",
                country=fake_address.country(),
                longitude=.123,
                latitude=.0123
            )
        )
    session.commit()


    for _ in range(N_ROUTES):
        session.add(
            Route(
                from_place_id=random.randint(1, N_PLACES),
                to_place_id=random.randint(1, N_PLACES),
            )
        )
    session.commit()

