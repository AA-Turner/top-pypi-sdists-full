from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)

from ...database import Base


class OrangeBookProductSubsidiaryModel(Base):
    __tablename__ = "orange_book_products_subsidiaries"

    id = Column(Integer, primary_key=True)
    orange_book_product_id = Column(
        Integer,
        ForeignKey('orange_book_products.id'),
        nullable=False,
    )
    subsidiary_id = Column(
        Integer,
        ForeignKey('subsidiaries.id'),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
