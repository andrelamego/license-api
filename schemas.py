from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

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
    consumer_id: Optional[str] = None
    consumed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LicenseVerifyRequest(BaseModel):
    key: str
    client_id: str   # identificador único enviado pelo cliente

class LicenseVerifyResponse(BaseModel):
    valid: bool
    reason: Optional[str] = None
    license: Optional[LicenseResponse] = None

    model_config = ConfigDict(from_attributes=True)