from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Text,
)

from ...database import Base


class ExternalDriveModel(Base):
    __tablename__ = "external_drives"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    org_id = Column(String(128), nullable=True)
    provider = Column(String(50), nullable=False)
    webhook_id = Column(String(128), nullable=False)
    additional_info = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
