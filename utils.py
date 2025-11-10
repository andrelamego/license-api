# utils.py
import uuid
from datetime import datetime, timedelta

def generate_license_key() -> str:
    """Generate a unique license key using UUID4."""
    return str(uuid.uuid4())

def calculate_expiration(days: int) -> datetime:
    """Calculate expiration date from current UTC time."""
    return datetime.utcnow() + timedelta(days=days)
