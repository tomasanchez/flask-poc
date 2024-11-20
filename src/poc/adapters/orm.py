from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.poc.model import Base

engine = create_engine("sqlite:////tmp/test.db")


def startup_db():
    """
    Start ups DB
    """
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
