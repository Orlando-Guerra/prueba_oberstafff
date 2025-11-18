# backend/models.py
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    user_id = Column(Text, primary_key=True)
    email = Column(Text, nullable=False)
    plan_type = Column(Text, nullable=False)
    status = Column(Text, nullable=False)  # 'trial', 'active', 'past_due', 'canceled'
    trial_ends_at = Column(DateTime)
    next_billing_at = Column(DateTime)
    last_payment_attempt = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
