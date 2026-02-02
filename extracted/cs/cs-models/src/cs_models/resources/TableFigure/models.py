from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Text,
    Boolean,
    ForeignKey,
)

from ...database import Base


class TableFigureModel(Base):
    __tablename__ = "table_figures"

    id = Column(Integer, primary_key=True)
    file_id = Column(
        Integer,
        ForeignKey('files.id'),
        nullable=True,
    )
    source_type = Column(String(50), nullable=False)
    source_id = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)
    label = Column(String(50), nullable=True)
    caption = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    link = Column(String(255), nullable=True)
    llm_processed = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
