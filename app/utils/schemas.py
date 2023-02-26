from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass


#update
class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True


