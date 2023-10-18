from pydantic import BaseModel

from domain.entities.user import User


class Account(BaseModel):
    user: User
