from sqlmodel import SQLModel, Session, create_engine
import os
from src.models.note import Note

engine = create_engine("sqlite:///database.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session