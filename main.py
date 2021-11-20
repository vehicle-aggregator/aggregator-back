from fastapi import FastAPI

from auth import app as auth_app

app = FastAPI()
app.mount('/auth', auth_app)



