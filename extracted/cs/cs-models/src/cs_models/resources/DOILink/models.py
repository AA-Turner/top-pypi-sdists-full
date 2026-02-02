from sqlalchemy import (
    Column,
    Integer,
    String,
    Binary,
)

from ...database import Base


class DOILinkModel(Base):
    __tablename__ = "doi_links"

    id = Column(Integer, primary_key=True)
    link = Column(
        Binary(16),
        nullable=False,
        index=True,
    )
    doi = Column(String(191), nullable=False)
