from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Text,
    Float,
    String,
    Boolean,
)

from ...database import Base


class SalesTableModel(Base):
    __tablename__ = "sales_tables"

    id = Column(Integer, primary_key=True)
    sec_accession_number = Column(String(128), nullable=False, index=True)
    sec_cik = Column(String(128), nullable=False)
    sec_file_name = Column(String(128), nullable=False)
    table_number = Column(Integer, nullable=False)
    table_preceding_info = Column(Text, nullable=True)
    table_html = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    processed = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
