from os import access
from typing import Literal, Union

from fastapi import FastAPI, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.params import Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
import pydantic

from model import Account, BusinessUser, CasualUser, User, UserIn, UserOut, engine



app =  FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_hashed_password(password: str) -> str:
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

def get_session():
    with Session(engine) as session:
        yield session


@app.post("/token")
async def login(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends()
    ):
    """По username и password выдаёт токен пользователя"""
    
    statement = select(User).where(User.email == form_data.username)\
                .where(User.hashed_password == get_hashed_password(form_data.password))
    try:
        user = session.exec(statement).one()
        return {"access_token": user.token, "token_type": "bearer"}
    except NoResultFound:
        raise HTTPException(status_code=403, detail="Incorrect username or password")


@app.post('/register', response_model=Account)
def register(
    session: Session = Depends(get_session),
    userin: UserIn = Body(...),
    type: Literal['casual', 'business'] = Body(...)):
    """Регистрация пользователя casual или business"""

    Account = dict(casual=CasualUser, business=BusinessUser)

    user = User(**userin.dict())
    user.hashed_password = get_hashed_password(userin.password)
    session.add(user)
    session.commit()
    session.refresh(user)

    account = Account[type](account_id=user.id)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account
        
    
@app.get('/me', response_model=UserOut)
async def get_me(user: User = Depends(get_current_active_user)):
    """Выдаёт данные текущего пользователя"""
    return UserOut(**user.dict())