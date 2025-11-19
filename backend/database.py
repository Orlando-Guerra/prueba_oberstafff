# backend/database.py - VERSIÓN CORREGIDA
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# VERIFICA que la variable se carga correctamente
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no encontrada en las variables de entorno")

print(f"Conectando a: {DATABASE_URL}")  # Para debug

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)