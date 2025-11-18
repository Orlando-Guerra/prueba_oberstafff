# backend/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubscriptionOut(BaseModel):
    user_id: str
    email: Optional[str] = None
    plan_type: Optional[str] = None
    status: str
    trial_ends_at: Optional[datetime] = None
    next_billing_at: Optional[datetime] = None
    last_payment_attempt: Optional[datetime] = None