# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from database import Base

class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(64), unique=True, index=True, nullable=False)
    plan = Column(String(50), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=False)  # keys nascem inativas
    created_at = Column(DateTime, default=datetime.utcnow)
    consumer_id = Column(String(128), nullable=True)   # novo: quem consumiu/associou
    consumed_at = Column(DateTime, nullable=True)      # opcional: quando consumiu (registro)
