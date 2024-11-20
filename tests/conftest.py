import pytest
from sqlalchemy import Engine, StaticPool, create_engine
from sqlalchemy.orm import Session

from src.poc.model import Base


@pytest.fixture(name="in_memory_db", scope="function")
def fixture_in_memory_db() -> Engine:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(name="session", scope="function")
def fixture_session(in_memory_db: Engine) -> Session:
    with Session(bind=in_memory_db) as session:
        yield session
