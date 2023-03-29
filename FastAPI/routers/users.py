from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


# User
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int


users_list = [
            User(id=1, name="Juan Diego", surname="Gallego Villada", age=23),
            User(id=2, name="Manuela", surname="Gallego Villada", age=20),
            User(id=3, name="Sara", surname="Gallego Villada", age=19)
            ]


router = APIRouter(prefix="/users",
                    tags=["users"], 
                    responses={404: {"message": "Not found!"}})


@router.get("/")
async def users():
    return users_list


# Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)


# Query
@router.get("/user/")
async def user(id: int):
    return search_user(id)


# Modifying the status code
@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        # return {"error": "User already exists!"}
        raise HTTPException(status_code=404, 
                            detail="User already exists!")
    else:
        users_list.append(user)
        # return {"success": "User added!"}
        return user


@router.put("/user/", status_code=201)
async def user(user: User):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        # return {"error": "User not updated!"}
        raise HTTPException(status_code=404, 
                            detail="User not updated!")
    else:
        return {"success": "User updated!"}


@router.delete("/user/{id}", status_code=200)
async def user(id: int):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    
    if not found:
        # return {"error": "User not deleted!"}
        raise HTTPException(status_code=404, 
                            detail="User not deleted!")
    else:
        return {"success": "User deleted!"}



def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found!"}



