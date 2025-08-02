from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Text,
)
from datetime import datetime

from ...database import Base


class UserWorkbookWorkflowsModel(Base):
    __tablename__ = 'user_workbook_workflows'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    is_active = Column(Boolean, nullable=True)
    workflow_template = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
