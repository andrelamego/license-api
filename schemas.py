# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LicenseBase(BaseModel):
    plan: str
    expires_at: datetime
    is_active: bool


class LicenseCreateRequest(BaseModel):
    plan: str
    duration_days: int


class LicenseResponse(BaseModel):
    id: int
    key: str
    plan: str
    expires_at: datetime
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class LicenseVerifyRequest(BaseModel):
    key: str


class LicenseVerifyResponse(BaseModel):
    valid: bool
    reason: Optional[str] = None
    license: Optional[LicenseResponse] = None
