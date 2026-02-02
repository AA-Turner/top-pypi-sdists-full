from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    String,
    Text,
)

from ...database import Base


class ScratchpadTableModel(Base):
    __tablename__ = "scratchpad_tables"

    id = Column(Integer, primary_key=True)
    source_type = Column(String(50), nullable=False)
    source_id = Column(
        Integer,
        nullable=False,
    )
    table_hash = Column(String(64), nullable=True)
    table_info = Column(Text, nullable=True)
    table_html_file_id = Column(
        Integer,
        ForeignKey('files.id'),
        nullable=True,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
