from sqlalchemy.orm import Session
from . import crud, models, schemas
from databases.core import Connection
from typing import Union, List
from pydantic import UUID4

from sqlalchemy.ext.asyncio import AsyncSession

from .crud import get_pillow_row, get_pillow, update_pillow, create_pillow, create_pillow_history


async def get_pillow_history(db: AsyncSession, user_id: int, uuid: UUID4) -> List[models.PillowsHistory]:
    res = await crud.get_pillow_history(db, user_id, uuid)
    print(res)
    return res


"""
-1 не задан id user или uuid
-2 нельзя произвести операцию с подушками
"""


async def create_pillow_with_history(db: AsyncSession, amount: int, user_id: int, uuid: UUID4):
    if user_id is None and uuid is None:
        return -1
    try:
        # Создаем запись в таблицу pillow_history
        cph = await create_pillow_history(db, user_id, uuid, amount)
        # debug
        # print("_____________CPH_____________________")
        # print(cph)
        # print("______________CPH____________________")
        # Идем во вторую таблицу и узнаем, есть ли там user_id
        db_pillow = await get_pillow(db, user_id, uuid)
        # если есть
        if db_pillow:
            # добавляем в таблицу значение amount
            db_pillow.num_pillows += amount
            if db_pillow.num_pillows >= 0:
                db_pillow = await update_pillow(db, db_pillow, user_id, uuid)
            else:
                # не хватает подушек
                return -2
        # если нет
        else:
            # если можно создать, создаем
            if amount >= 0:
                await create_pillow(db, user_id, uuid, amount)
            else:
                # не хватает подушек
                return -2

        await db.commit()
        return 0
    except:
        # Rollback the transaction in case of error
        await db.rollback()
        raise
