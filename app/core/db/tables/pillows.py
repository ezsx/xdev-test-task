# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, text
from sqlalchemy.dialects.postgresql import UUID
from core.db.db_session import Base



class Pillow(Base):
    __tablename__ = 'pillows'

    id = Column(Integer, primary_key=True, server_default=text("nextval('pillows_id_seq'::regclass)"))
    user_id = Column(Integer, nullable=False)
    device_uuid = Column(UUID)
    num_pillows = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
