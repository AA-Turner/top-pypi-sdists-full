from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
)

from ...database import Base


class VAParameterViewModel(Base):
    __tablename__ = "va_parameter_views"

    id = Column(Integer, primary_key=True)
    user_va_parameter_view_id = Column(
        Integer,
        ForeignKey('user_va_parameter_views.id'),
        nullable=False,
    )
    va_parameter_id = Column(
        Integer,
        ForeignKey('va_parameters.id'),
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
