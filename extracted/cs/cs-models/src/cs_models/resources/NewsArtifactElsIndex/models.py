from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
)

from ...database import Base


class NewsArtifactElsIndexModel(Base):
    __tablename__ = "news_artifacts_els_index"

    id = Column(Integer, primary_key=True)
    artifact_id = Column(
        String(50),
        nullable=False,
        index=True
    )
    els_indexed = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
