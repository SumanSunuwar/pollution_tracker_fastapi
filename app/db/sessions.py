from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import CORE_SETTINGS

engine = create_engine(CORE_SETTINGS.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
