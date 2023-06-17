from pydantic import BaseModel, Field

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