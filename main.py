from fastapi import FastAPI
from sqlmodel.orm.session import Session

from auth import app as auth_app
from model import create_db_and_tables, engine
from vehicle import app as vehicle_app
from company import app as company_app

app = FastAPI()
app.mount('/auth', auth_app)
app.mount('/vehicle', vehicle_app)
app.mount('/company', company_app)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()



