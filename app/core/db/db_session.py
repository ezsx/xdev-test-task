from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
from include.config import Settings


settings = Settings()
print("__________________________________", str(settings.DB_URL))
engine = create_async_engine(settings.DB_URL,
                             pool_pre_ping=True,
                             echo=True,
                             pool_size=settings.DB_MIN_CONNECTIONS,
                             max_overflow=settings.DB_MAX_CONNECTIONS
                             )
                             # pool_timeout=30,
                             # connect_args={"server_settings": {"application_name": settings.PROJECT_NAME}})  # noqa E501

async_session = sessionmaker(autocommit=False,
                             autoflush=False,
                             bind=engine,
                             class_=AsyncSession)

Base = declarative_base()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
