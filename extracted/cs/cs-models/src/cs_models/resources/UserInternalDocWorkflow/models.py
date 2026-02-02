from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
)
from datetime import datetime

from ...database import Base


class UserInternalDocWorkflowModel(Base):
    __tablename__ = 'user_internal_doc_workflow'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False, index=True)
    internal_doc_workflow = Column(
        Text,
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
