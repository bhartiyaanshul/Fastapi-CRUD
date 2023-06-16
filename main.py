from fastapi import FastAPI
from pydantic import BaseModel, Field
import databases,sqlalchemy,uuid,datetime


app = FastAPI()

DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1:5432/usertest"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "py_users",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.String,primary_key=True),
    sqlalchemy.Column("username",sqlalchemy.String),
    sqlalchemy.Column("password",sqlalchemy.String),
    sqlalchemy.Column("first_name",sqlalchemy.String),
    sqlalchemy.Column("last_name",sqlalchemy.String),
    sqlalchemy.Column("gender",sqlalchemy.CHAR),
    sqlalchemy.Column("create_at",sqlalchemy.String),
    sqlalchemy.Column("status",sqlalchemy.CHAR)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)

metadata.create_all(engine)

#Models

class userList(BaseModel):
    id : str
    username: str
    password: str
    first_name: str
    last_name: str
    gender: str
    create_at: str
    status: str
    
class userEntry(BaseModel):
    username    : str = Field(..., example="anshul")
    password    : str = Field(..., example="anshul")
    first_name  : str = Field(..., example="anshul")
    last_name   : str = Field(..., example="Bhartiya")
    gender      : str = Field(..., example="M")
    
class userUpdate(BaseModel):
    id    : str = Field(..., example="Enter a id")
    first_name  : str = Field(..., example="anshul")
    last_name   : str = Field(..., example="Bhartiya")
    gender      : str = Field(..., example="M")
    status      : str = Field(..., example="1")
    
class userDelete(BaseModel):
    id    : str = Field(..., example = "Enter a id")
    
#CRUD
    
@app.on_event("startup")
async def startup():
    await database.connect()
    
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect() 
    
@app.get("/user", response_model=list[userList])
async def get_all_users():
    query = users.select()
    return await database.fetch_all(query)

@app.get("/users/{userId}",response_model=userList)
async def find_user_by_id(userId : str):
    query = users.select().where(users.c.id == userId)
    return await database.fetch_one(query)

@app.post("/user",response_model=userList)
async def register_user(user : userEntry):
    gID = str(uuid.uuid1())
    gDate = str(datetime.datetime.now())
    query = users.insert().values(
        id = gID,
        username = user.username,
        password = user.password,
        first_name = user.first_name,
        last_name = user.last_name,
        gender = user.gender,
        create_at = gDate,
        status = "1"
    )
    await database.execute(query)
    return {
        "id":gID,
        **user.dict(),
        "create_at":gDate,
        "status":"1"   
    }
    
@app.put("/user",response_model=userList)
async def update_user(user : userUpdate):
    gDate = str(datetime.datetime.now())
    query = users.update().\
        where(users.c.id == user.id).\
        values(
            first_name = user.first_name,
            last_name = user.last_name,
            gender = user.gender,
            status = user.status,
            create_at = gDate,   
        )
    await database.execute(query)
        
    return await find_user_by_id(user.id)

@app.delete("/user/{userId}")
async def delete_user(user : userDelete):
    query = users.delete().where(users.c.id == user.id)
    await database.execute(query)
    
    return{
        "status":True,
        "message":"Your user has been deleted successfully"
    }
    
    


