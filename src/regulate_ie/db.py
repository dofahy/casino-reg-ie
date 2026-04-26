import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

_engine = None
_SessionLocal = None


def get_database_url() -> str:
    return (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )


def init_engine():
    global _engine, _SessionLocal
    if _engine is None:
        database_url = get_database_url()
        _engine = create_engine(database_url, echo=False)
        _SessionLocal = sessionmaker(bind=_engine)
    return _engine


def get_engine():
    if _engine is None:
        raise RuntimeError("Need to call init_engine()")
    return _engine


def get_session():
    if _SessionLocal is None:
        raise RuntimeError("Need to call init_engine()")
    return _SessionLocal()
