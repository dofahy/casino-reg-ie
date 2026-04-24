from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from casino_reg_ie.db import Base


class Regulation(Base):
    __tablename__ = 'regulations'

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
