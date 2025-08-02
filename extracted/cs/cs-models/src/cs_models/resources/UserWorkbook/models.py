from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class UserWorkbookModel(Base):
    __tablename__ = 'user_workbooks'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    is_active = Column(Boolean, nullable=True)
    workbook_id = Column(
        Integer,
        ForeignKey('workbooks.id'),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
