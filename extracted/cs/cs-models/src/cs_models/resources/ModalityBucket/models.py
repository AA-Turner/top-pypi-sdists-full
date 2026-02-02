from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from datetime import datetime

from ...database import Base


class ModalityBucketModel(Base):
    __tablename__ = 'modality_buckets'

    id = Column(Integer, primary_key=True)
    modality_bucket = Column(String(50), unique=True, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
