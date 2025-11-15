from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

Base = declarative_base()
engine = create_engine(SUPABASE_DB_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class Metric(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    cpu_percent = Column(Float)
    memory_percent = Column(Float)
    disk_percent = Column(Float)

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    alert = Column(String)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("✅ Tables created successfully on Supabase!")
