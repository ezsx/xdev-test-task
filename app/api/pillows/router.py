from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from loguru import logger as log

from core.db.pool import Connection, DBConnPool

router = APIRouter()


@cbv(router)
class PillowsRouter:
    # prefix = "/pillows
    conn: Connection = Depends(DBConnPool().get_connection)

    @router.get(
        "/",
        name="Получить количество подушек"
    )
    async def get_pillows(
            self
    ):
        pass
