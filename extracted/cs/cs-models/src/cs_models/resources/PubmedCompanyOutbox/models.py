from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)

from ...database import Base


class PubmedCompanyOutboxModel(Base):
    __tablename__ = 'pubmed_company_outbox'

    id = Column(Integer, primary_key=True)
    pubmed_id = Column(
        Integer,
        ForeignKey('pubmed.id'),
        nullable=False,
    )
    entity_name = Column(String(256), nullable=False)
