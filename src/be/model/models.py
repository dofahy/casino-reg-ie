from sqlalchemy import Column, DateTime, Integer, String, Text
from datetime import datetime, UTC
from be.db import Base

class Regulation(Base):
    __tablename__ = "regulations"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
