import logging

from fastapi import FastAPI

from loguru import logger as log

# from core.events import Events
from starlette.middleware.cors import CORSMiddleware
from core.db.db_session import init_models
from api.router import main_router


app = FastAPI(
    title="Microservice Test Task API methods",
    version="0.0.1",
    openapi_tags=[{"name": "Test Task", "description": "Test Task Requests"}]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# @app.on_event("startup")
# def start_db():
#     # await init_models()
#     logging.info('=> init models pass...ok')
#     print('=> init models pass...ok')

# events = Events(have_db=True)
# app.add_event_handler("startup", events.get_startup())
# app.add_event_handler("shutdown", events.get_shutdown())

app.include_router(main_router)
