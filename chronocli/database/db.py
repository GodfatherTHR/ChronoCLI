import os
from sqlmodel import SQLModel, create_engine, Session, select
from chronocli.models.models import Session as TrackingSession
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "chronocli.db")
sqlite_url = f"sqlite:///{DB_PATH}"

engine = create_engine(sqlite_url, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

def get_active_session():
    with get_session() as session:
        statement = select(TrackingSession).where(TrackingSession.end_time == None)
        return session.exec(statement).first()
