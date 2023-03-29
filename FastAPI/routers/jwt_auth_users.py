from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "83b986364a563c343637ee8969fadbc1cf93012b3650acc08da18a7e14eea901"

router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={404: {"message": "Not found!"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])



class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "juandiego": {
        "username": "juandiego",
        "full_name": "Juan Diego Gallego Villada",
        "email": "juandiego99@correo.com",
        "disabled": False,
        "password": "$2a$12$O2K291hYThS7hCyzBQWg6OcVRUSNu/OixikVcdPjWL41hQHZE8tte"
    },
    "juandiego2": {
        "username": "juandiego2",
        "full_name": "Juan Diego Gallego Villada 2",
        "email": "juandiego299@correo.com",
        "disabled": True,
        "password": "$2a$12$FhDPrNvuJbIblPGR7J3QOuhpGb10d2HHeBCCdWNvYmAllx.JYeXLi"
    }
}


def search_user_db(username: str):
    if username in users_db:
        # ** indicates that I could pass multiple parameters (**kwargs)!!
        return UserDB(**users_db[username])


def search_user(username: str):

    if username in users_db:
        # ** indicates that I could pass multiple parameters (**kwargs)!!
        return User(**users_db[username])


async def auth_user(token: str=Depends(oauth2)):
    
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid auth credentials", 
        headers={"www.authenticate": "jwt"})

    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception
    
    return search_user(username)
    

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is disabled!")
    
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm=Depends()):
    
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Wrong username!")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Wrong password!")
    
    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, key=SECRET, algorithm=ALGORITHM), "token_type": "jwt"}



@router.get("/users/me")
async def me(user: User=Depends(current_user)):
    return user