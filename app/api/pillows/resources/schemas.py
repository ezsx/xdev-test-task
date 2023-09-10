from datetime import datetime
from typing import Union
from pydantic import UUID4

from pydantic import BaseModel, Field


class PillowsAmount(BaseModel):
    user_id: Union[int, None] = Field(description='Идентификатор пользователя в бд')
    uuid: Union[UUID4, None] = Field(description='Идентификатор устройства в бд')
    amount: int = Field(description='Количество подушек пользователя')

class PillowsHistory(BaseModel):
    user_id: Union[int, None] = Field(description='Идентификатор пользователя в бд')
    uuid: Union[UUID4, None] = Field(description='Идентификатор устройства в бд')
    amount: int = Field(description='Количество подушек пользователя')
    created_at: datetime = Field(description='Количество подушек пользователя')
