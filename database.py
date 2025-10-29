from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://avnadmin:AVNS_p5QpL_bEKTouPQA4IrJ@geloice-geloice.f.aivencloud.com:10509/GeloIceDB?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
