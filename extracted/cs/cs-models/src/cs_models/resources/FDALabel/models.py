from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    Boolean,
)
from datetime import datetime
from ...database import Base


class FDALabelModel(Base):
    __tablename__ = 'fda_labels'

    id = Column(Integer, primary_key=True)
    set_id = Column(String(128), nullable=False, index=True)
    doc_id = Column(String(128), nullable=False)
    date = Column(DateTime, nullable=False)
    version = Column(String(20), nullable=False)
    section_id = Column(String(128), nullable=False)
    section_type = Column(String(20), nullable=False)
    section_html_file_id = Column(
        Integer,
        ForeignKey('files.id'),
        nullable=True,
    )
    label_html_file_id = Column(
        Integer,
        ForeignKey('files.id'),
        nullable=False,
    )
    section_text = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=True)
    vector_active = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
