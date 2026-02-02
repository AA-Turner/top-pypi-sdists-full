from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
    String,
    Text,
)

from ...database import Base


class DrugIndicationTableModel(Base):
    __tablename__ = "drug_indications_tables"

    id = Column(Integer, primary_key=True)
    drug_indication_id = Column(
        Integer,
        ForeignKey('drug_indications.id'),
        nullable=False,
    )
    table_text = Column(Text, nullable=False)
    table_info = Column(Text, nullable=True)
    table_hash = Column(String(64), nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
