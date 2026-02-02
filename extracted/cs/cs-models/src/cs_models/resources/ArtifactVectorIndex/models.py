from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    String,
)

from ...database import Base


class ArtifactVectorIndexModel(Base):
    __tablename__ = "artifact_vector_index"

    id = Column(Integer, primary_key=True)
    artifact_id = Column(
        String(50),
        nullable=False,
        index=True,
    )
    embedding_created = Column(Boolean, nullable=True)
    embedding_s3_key = Column(String(128), nullable=True)
    vector_indexed = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
