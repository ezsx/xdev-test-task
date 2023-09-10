from typing import Union, List
from pydantic import UUID4
from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from loguru import logger as log
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.pool import Connection, DBConnPool
from api.pillows.resources.service import create_pillow_with_history, get_pillow_history
from core.db.db_session import get_session
from api.pillows.resources.crud import get_pillows

from api.pillows.resources.schemas import PillowsAmount, PillowsHistory

router = APIRouter()


@cbv(router)
class PillowsRouter:
    # prefix = "/pillows
    # conn: Connection = Depends(DBConnPool().get_connection)
    sess: AsyncSession = Depends(get_session)

    @router.get(
        "/get_amount_pillows",
        name="Получить количество подушек"
        # response_model=PillowsAmount
    )
    async def api_get_pillows(
            self,
            user_id: Union[int, None] = None,
            uuid: Union[UUID4, None] = None
    ) -> PillowsAmount:
        amount = await get_pillows(self.sess, user_id, uuid)
        return PillowsAmount(user_id=user_id,
                             uuid=uuid,
                             amount=amount
                             )

    @router.get(
        "/get_pillows_history",
        name="история начисления и списания подушек конкретного пользователя"
    )
    async def api_get_history(
            self,
            user_id: Union[int, None] = None,
            uuid: Union[UUID4, None] = None
    ) -> List[PillowsHistory]:
        result = await get_pillow_history(self.sess, user_id, uuid)
        list_result = []
        for r in result:
            # r = rr._asdict()
            print("r____________", r)
            temp = PillowsHistory(
                user_id=r.user_id,
                uuid=r.device_uuid,
                amount=r.amount,
                created_at=r.created_at
            )
            list_result.append(temp)
        return list_result

    @router.post(
        "/post",
        name="Изменить количество подушек",
        description="Возвращает если: 0 ОК, -1 у пользователя нет подушек, -2 подушек не хватает для списания"

    )
    async def api_create_pillows_history(
            self,
            amount: int,
            user_id: Union[int, None] = None,
            uuid: Union[UUID4, None] = None
    ):
        print("_____________router create pillows")
        result = await create_pillow_with_history(self.sess, amount, user_id, uuid)
        return result

