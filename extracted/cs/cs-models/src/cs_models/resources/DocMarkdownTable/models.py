from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
)

from ...database import Base


class DocMarkdownTableModel(Base):
    __tablename__ = "doc_markdown_tables"

    id = Column(Integer, primary_key=True)
    artifact_id = Column(String(50), nullable=False, index=True)
    markdown_table = Column(Text, nullable=False)
    markdown_table_description = Column(Text, nullable=True)
    has_table_description = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
