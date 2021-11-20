from os import access

from fastapi import FastAPI, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
import pydantic 

from model import User, UserIn, UserOut, engine



app =  FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_hashed_password(password: str) -> str:
    return password


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    with Session(engine) as session:
        statement = select(User).where(User.token == token)
        try:
            user = session.exec(statement).one()
            return user
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """По username и password выдаёт токен пользователя"""
    with Session(engine) as session:
        statement = select(User).where(User.email == form_data.username)\
                    .where(User.hashed_password == get_hashed_password(form_data.password))
        try:
            user = session.exec(statement).one()
            return {"access_token": user.token, "token_type": "bearer"}
        except NoResultFound:
            raise HTTPException(status_code=403, detail="Incorrect username or password")


@app.post('/register')
async def register(user: UserIn):
    """Регистрация пользователя"""
    with Session(engine) as session:
        session.add(
            User(**user.dict())
        )
    

@app.get('/me', response_model=UserOut)
async def get_me(user: User = Depends(get_current_active_user)):
    """Выдаёт данные текущего пользователя"""
    return UserOut(**user.dict())