import datetime
from typing import List

from pydantic import UUID4
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


async def create_pillow_history(db: AsyncSession, user_id: int, uuid: UUID4, amount: int):
    db_pillow = models.PillowsHistory(user_id=user_id,
                                      device_uuid=uuid,
                                      amount=amount,
                                      created_at=datetime.datetime.now())
    db.add(db_pillow)
    await db.commit()
    await db.refresh(db_pillow)
    return db_pillow


# Pillow CRUD
# запрос для получения количества подушек конкретного пользователя
async def get_pillows(db: AsyncSession, user_id: int = None, uuid: UUID4 = None) -> int:
    if user_id:
        q = select(func.sum(models.Pillow.num_pillows)).where(models.Pillow.user_id == user_id)
        res = await db.execute(q)
        return res.scalar() or 0
    if uuid:
        q = select(func.sum(models.Pillow.num_pillows)).where(models.Pillow.device_uuid == uuid)
        res = await db.execute(q)
        return res.scalar() or 0
    return 0


# запрос для получения истории начисления и списания подушек конкретного пользователя
async def get_pillow_history(db: AsyncSession, user_id: int, uuid: UUID4) -> List[models.PillowsHistory]:
    if user_id:
        q = select(models.PillowsHistory).where(models.PillowsHistory.user_id == user_id)
        print("q________", str(q))
        res = await db.execute(q)
        return res.scalars().all()
    if uuid:
        q = select(models.PillowsHistory).where(models.PillowsHistory.device_uuid == uuid)
        res = await db.execute(q)
        return res.scalars().all()


# делаем запрос к Pillow и получаем инфу о пользователе с подушками
async def get_pillow(db: AsyncSession, user_id: int = None, uuid: UUID4 = None) -> models.Pillow:
    if user_id:
        q = select(models.Pillow).where(models.Pillow.user_id == user_id)
        res = await db.execute(q)
        return res.scalars().first()
    if uuid:
        q = select(models.Pillow).where(models.Pillow.uuid == uuid)
        res = await db.execute(q)
        return res.scalars().first()


async def get_pillow_row(db: AsyncSession, user_id: int = None, uuid: UUID4 = None) -> models.Pillow:
    if user_id:
        q = select(models.Pillow).where(models.Pillow.user_id == user_id)
        res = await db.execute(q)
        return res.first()
    if uuid:
        q = select(models.Pillow).where(models.Pillow.uuid == uuid)
        res = await db.execute(q)
        return res.first()


async def create_pillow(db: AsyncSession, user_id: int, uuid: UUID4, num_pillows: int):
    db_pillow = models.Pillow(user_id=user_id,
                              device_uuid=uuid,
                              num_pillows=num_pillows,
                              created_at=datetime.datetime.now())
    db.add(db_pillow)
    await db.commit()
    await db.refresh(db_pillow)
    return db_pillow


async def update_pillow(db: AsyncSession, pillow: models.Pillow = None, user_id: int = None,
                        uuid: UUID4 = None) -> models.Pillow:
    db_pillow = None
    if user_id:
        q = select(models.Pillow).where(models.Pillow.user_id == user_id)
        res = await db.execute(q)
        db_pillow = res.scalars().first()
    elif uuid:
        q = select(models.Pillow).where(models.Pillow.uuid == uuid)
        res = await db.execute(q)
        db_pillow = res.scalars().first()
    if db_pillow:
        # col_obj: sqlalchemy.schema.Column
        for col_obj in models.Pillow.__table__.columns:
            col = col_obj.name
            if hasattr(db_pillow, col):
                setattr(db_pillow, col, getattr(pillow, col))
        await db.commit()
        await db.refresh(db_pillow)
        return db_pillow

    return None
