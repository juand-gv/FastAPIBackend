from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId


router = APIRouter(prefix="/usersdb",
                    tags=["usersdb"], 
                    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found!"}})


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


# Path
@router.get("/user/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


# Query
@router.get("/user/")
async def user(id: str):
    return search_user("_id", ObjectId(id))


# Modifying the status code
@router.post("/user/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
        
        if type(search_user("email", user.email)) == User:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="User already exists!")

        user_dict = dict(user)
        del user_dict["id"]
        
        id = db_client.users.insert_one(user_dict).inserted_id
        new_user = user_schema(db_client.users.find_one({"_id": id}))

        return User(**new_user)


@router.put("/user/", status_code=status.HTTP_201_CREATED)
async def user(user: User):
    
    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "User not updated!"}
    
    return search_user("_id", ObjectId(user.id))



@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not deleted!")
    else:
        return {"success": "User deleted!"}


def search_user(field: str, key):
    
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))

    except:
        return {"error": "User not found!"}



