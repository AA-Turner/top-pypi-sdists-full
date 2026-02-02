from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
)
from datetime import datetime

from ...database import Base


class UserOrganizationModel(Base):
    __tablename__ = 'user_organizations'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False, unique=True)
    organization_id = Column(String(128), nullable=False, index=True)
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
