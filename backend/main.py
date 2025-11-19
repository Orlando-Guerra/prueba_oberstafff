# backend/main.py - VERSIÓN CON DEBUGGING
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List
from sqlalchemy import text
from .database import SessionLocal
from .schemas import SubscriptionOut
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Configuración CORS
origins = ["http://localhost:5500", "http://127.0.0.1:5500", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "¡API de Suscripciones funcionando!"}

@app.get("/subscription/{user_id}", response_model=SubscriptionOut)
def get_subscription(user_id: str):
    logger.debug(f"🔍 Buscando usuario: {user_id}")
    
    try:
        with SessionLocal() as db:
            logger.debug("✅ Conexión a BD establecida")
            
            result = db.execute(
                text("SELECT * FROM subscriptions WHERE user_id = :user_id"),
                {"user_id": user_id}
            )
            subscription = result.fetchone()
            
            logger.debug(f"📊 Resultado de BD: {subscription}")
            
            if not subscription:
                logger.warning(f"❌ Usuario no encontrado: {user_id}")
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            subscription_dict = dict(subscription._mapping)
            logger.debug(f"✅ Usuario encontrado: {subscription_dict}")
            
            return subscription_dict
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error de base de datos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Endpoint para ver TODOS los usuarios
@app.get("/all-users")
def get_all_users():
    try:
        with SessionLocal() as db:
            result = db.execute(text("SELECT user_id, email, status FROM subscriptions"))
            users = [dict(row._mapping) for row in result]
            return {"users": users}
    except Exception as e:
        return {"error": str(e)}