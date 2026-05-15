from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_name: str
    category: Optional[str] = "Personal"
    tags: Optional[str] = ""  # Stored as comma-separated
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration: Optional[float] = 0.0  # Seconds
    notes: Optional[str] = None
    is_paused: bool = Field(default=False)
    last_pause_time: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    color: Optional[str] = "white"

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

class AILog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prompt: str
    response: str
    feature: str  # e.g., 'weekly_analysis', 'coach', 'nlp'
    created_at: datetime = Field(default_factory=datetime.now)

class Setting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    value: str
