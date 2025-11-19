# backend/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SubscriptionOut(BaseModel):
    user_id: str
    email: str
    plan_type: str
    status: str
    trial_ends_at: Optional[datetime] = None
    next_billing_at: Optional[datetime] = None
    last_payment_attempt: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True