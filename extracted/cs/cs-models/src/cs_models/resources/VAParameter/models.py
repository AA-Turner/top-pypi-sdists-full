from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
)
from datetime import datetime

from ...database import Base


class VAParameterModel(Base):
    __tablename__ = 'va_parameters'

    id = Column(Integer, primary_key=True)
    pid = Column(Integer, nullable=False, index=True)
    cid = Column(Integer, nullable=False, index=True)
    pname = Column(String(191), nullable=False)
    ciso = Column(String(20), nullable=True)
    u = Column(Integer, nullable=True)
    sign = Column(String(10), nullable=True)
    ppid = Column(Integer, nullable=True, index=True)
    ftid = Column(Integer, nullable=True)
    dpname = Column(String(191), nullable=True)
    scid = Column(Integer, nullable=True)
    so = Column(Integer, nullable=True)
    llm_output = Column(Text, nullable=True)
    needs_review = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
