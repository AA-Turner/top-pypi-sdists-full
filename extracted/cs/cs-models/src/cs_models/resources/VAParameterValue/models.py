from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class VAParameterValueModel(Base):
    __tablename__ = 'va_parameter_values'

    id = Column(Integer, primary_key=True)
    va_parameter_id = Column(
        Integer,
        ForeignKey('va_parameters.id'),
        nullable=False,
    )
    pid = Column(Integer, nullable=False, index=True)
    cid = Column(Integer, nullable=False, index=True)
    sid = Column(Integer, nullable=False, index=True)
    r = Column(DateTime, nullable=True)
    p = Column(String(50), nullable=True)
    ap = Column(String(50), nullable=True)
    v = Column(Float, nullable=True)
    ciso = Column(String(20), nullable=True)
    csym = Column(String(10), nullable=True)
    u = Column(Integer, nullable=True)
    mdt = Column(DateTime, nullable=True)
    vt = Column(String(20), nullable=True)
    dt = Column(String(5), nullable=True)
    b = Column(Integer, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
