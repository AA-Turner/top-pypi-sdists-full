from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
)

from ...database import Base


class ModalityBucketMapModel(Base):
    __tablename__ = "modality_bucket_map"

    id = Column(Integer, primary_key=True)
    modality_id = Column(
        Integer,
        ForeignKey('modalities.id'),
        nullable=False,
    )
    modality_bucket_id = Column(
        Integer,
        ForeignKey('modality_buckets.id'),
        nullable=False,
    )
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
