from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(prefix="/basicauth",
                   tags=["basicauth"],
                   responses={404: {"message": "Not found!"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "password": "123456"
    },
    "juandiego2": {
        "username": "juandiego2",
        "full_name": "Juan Diego Gallego Villada 2",
        "email": "juandiego299@correo.com",
        "disabled": True,
        "password": "654321"
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


async def current_user(token: str = Depends(oauth2)):
    user =  search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid auth credentials", 
            headers={"www.authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is disabled!", 
            headers={"www.authenticate": "Bearer"})
    
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm=Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Wrong username!")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Wrong password!")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User=Depends(current_user)):
    return user
