import traceback
from contextlib import suppress
from typing import Callable

from loguru import logger as log

from core.db.pool import DBConnPool
from include import config


class Events:
    def __init__(
            self,
            have_db: bool = False,
            have_redis: bool = False,
            exit_on_fail: bool = True
    ):
        self._have_db = have_db
        self._have_redis = have_redis
        self._exit_on_fail = exit_on_fail

    def get_startup(self) -> Callable:
        async def startup():
            log.info(f"START service {config.SERVICE_NAME}")

            try:
                if self._have_db:
                    log.info(f"*** Connecting to DB '{config.DB_DB}' at {config.DB_HOST}:{config.DB_PORT}")
                    await DBConnPool().init_db()
                    log.info(f"*** Connected to DB '{config.DB_DB}' at {config.DB_HOST}:{config.DB_PORT}")

            except Exception as e:
                log.error(f"*** Startup exception ({repr(e)}): {traceback.format_exc()}")
                if self._exit_on_fail:
                    exit()
                else:
                    raise

            log.info(f"Service {config.SERVICE_NAME} started successfully")

        return startup

    def get_shutdown(self) -> Callable:
        async def shutdown():
            log.info(f"Shutdown service {config.SERVICE_NAME}")

            if self._have_db:
                with suppress(Exception):
                    await DBConnPool().close_db()

            log.info(f"Service {config.SERVICE_NAME} stopped successfully")

        return shutdown
