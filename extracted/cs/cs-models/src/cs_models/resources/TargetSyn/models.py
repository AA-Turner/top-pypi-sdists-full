from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class TargetSynModel(Base):
    __tablename__ = 'target_syns'

    id = Column(Integer, primary_key=True)
    synonym = Column(String(191), nullable=False, index=True)
    target_id = Column(
        Integer,
        ForeignKey('targets.id'),
        nullable=True,
    )
    source = Column(String(50), nullable=True)
    obsolete = Column(Boolean, nullable=True)
    synonym_type = Column(String(50), nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
