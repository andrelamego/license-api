# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, SessionLocal
from models import License
from schemas import (
    LicenseCreateRequest,
    LicenseResponse,
    LicenseVerifyRequest,
    LicenseVerifyResponse,
)
from utils import generate_license_key, calculate_expiration

app = FastAPI(title="License Key API", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria a tabela no banco
Base.metadata.create_all(bind=engine)


# ----------------------------
# Sessão do banco
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------
# Rotas
# ----------------------------
@app.get("/")
def root():
    return {"message": "License Key API is running 🚀"}


@app.post("/license/create", response_model=LicenseResponse)
def create_license(payload: LicenseCreateRequest, db: Session = Depends(get_db)):
    key = generate_license_key()
    expires_at = calculate_expiration(payload.duration_days)
    license_obj = License(
        key=key,
        plan=payload.plan,
        expires_at=expires_at,
        is_active=False,
    )
    db.add(license_obj)
    db.commit()
    db.refresh(license_obj)
    return license_obj


from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime

from models import License
from schemas import LicenseVerifyRequest, LicenseVerifyResponse, LicenseResponse
from database import SessionLocal



# verify & bind endpoint
@app.post("/license/verify", response_model=LicenseVerifyResponse)
def verify_license(payload: LicenseVerifyRequest, db: Session = Depends(get_db)):
    """
    Verifica a key e realiza bind ao client_id no primeiro uso.

    Regras:
    - not found -> reason "not found"
    - expired -> reason "expired"
    - if consumer_id is None -> bind to payload.client_id, set is_active True, set consumed_at
    - if consumer_id == payload.client_id -> valid True (same owner)
    - if consumer_id != payload.client_id -> reason "bound_to_another_client"
    """
    license_obj = db.query(License).filter(License.key == payload.key).first()

    if not license_obj:
        return LicenseVerifyResponse(valid=False, reason="not found")

    # check expiration first
    if license_obj.expires_at < datetime.utcnow():
        return LicenseVerifyResponse(valid=False, reason="expired")

    # if no consumer bound yet -> bind to this client_id (first use)
    if license_obj.consumer_id is None:
        license_obj.consumer_id = payload.client_id
        license_obj.is_active = True
        license_obj.consumed_at = datetime.utcnow()
        db.commit()
        db.refresh(license_obj)

        license_data = LicenseResponse.model_validate(license_obj, from_attributes=True)
        return LicenseVerifyResponse(valid=True, license=license_data)

    # if it is bound to a different client -> reject
    if license_obj.consumer_id != payload.client_id:
        return LicenseVerifyResponse(valid=False, reason="bound_to_another_client")

    # same consumer -> ok (still valid if not expired)
    license_data = LicenseResponse.model_validate(license_obj, from_attributes=True)
    return LicenseVerifyResponse(valid=True, license=license_data)



@app.get("/licenses", response_model=list[LicenseResponse])
def list_licenses(db: Session = Depends(get_db)):
    """List all license keys."""
    licenses = db.query(License).all()
    return licenses


@app.put("/license/deactivate/{license_id}", response_model=LicenseResponse)
def deactivate_license(license_id: int, db: Session = Depends(get_db)):
    """Deactivate a license key."""
    license_obj = db.query(License).filter(License.id == license_id).first()
    if not license_obj:
        raise HTTPException(status_code=404, detail="License not found")

    license_obj.is_active = False
    db.commit()
    db.refresh(license_obj)
    return license_obj


@app.put("/license/renew/{license_id}", response_model=LicenseResponse)
def renew_license(license_id: int, db: Session = Depends(get_db)):
    """Renew a license key for +30 days."""
    license_obj = db.query(License).filter(License.id == license_id).first()
    if not license_obj:
        raise HTTPException(status_code=404, detail="License not found")

    license_obj.expires_at = license_obj.expires_at + timedelta(days=30)
    db.commit()
    db.refresh(license_obj)
    return license_obj
