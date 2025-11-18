# backend/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from typing import List
from .schemas import SubscriptionOut  # Importa el modelo Pydantic

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡API de Suscripciones funcionando!"}

@app.get("/subscriptions", response_model=List[SubscriptionOut])
def get_subscriptions():
    # Devuelve una lista de suscripciones de ejemplo
    return [
        {
            "user_id": "user_001",
            "email": "user1@test.com",
            "plan_type": "pro",
            "status": "active",
            "trial_ends_at": None,
            "next_billing_at": None,
            "last_payment_attempt": None
        },
        {
            "user_id": "user_002",
            "email": "user2@test.com",
            "plan_type": "basic",
            "status": "trial",
            "trial_ends_at": None,
            "next_billing_at": None,
            "last_payment_attempt": None
        }
    ]

@app.get("/test")
def test_endpoint():
    return {"status": "success", "message": "Todo funciona correctamente"}