from fastapi import APIRouter, HTTPException
from config.koneksi import connect_to_db
from schema.userSchema import userEntity, usersEntity
from models.users import User
from bson import ObjectId

user = APIRouter()

db = connect_to_db()
if db is not None:
    user_collection = db['users'] 


@user.get('/')
async def find_all_users():
    try:
        users = user_collection.find()  
        return usersEntity(users)
    except Exception as e:
        return {"error": str(e)}


@user.post('/')
async def create_user(user: User):
    try:
        new_user = dict(user)  
        result = user_collection.insert_one(new_user)  
        return userEntity(user_collection.find_one({"_id": result.inserted_id}))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user.get('/{id}')
async def find_user_by_id(id: str):
    try:
        user = user_collection.find_one({"_id": ObjectId(id)})  
        if user:
            return userEntity(user)
        raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user.put('/{id}')
async def update_user(id: str, user: User):
    try:
        updated_user = dict(user)
        result = user_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_user})
        if result.modified_count == 1:
            return userEntity(user_collection.find_one({"_id": ObjectId(id)}))
        raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user.delete('/{id}')
async def delete_user(id: str):
    try:
        result = user_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return {"message": "Pengguna berhasil dihapus"}
        raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
