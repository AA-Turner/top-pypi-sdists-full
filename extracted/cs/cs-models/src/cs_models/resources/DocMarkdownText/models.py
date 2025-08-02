from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
)

from ...database import Base


class DocMarkdownTextModel(Base):
    __tablename__ = "doc_markdown_texts"

    id = Column(Integer, primary_key=True)
    source_type = Column(String(50), nullable=False)
    source_id = Column(Integer, nullable=False)
    markdown_text = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
