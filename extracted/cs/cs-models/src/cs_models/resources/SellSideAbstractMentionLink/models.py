from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class SellSideAbstractMentionLinkModel(Base):
    __tablename__ = "sell_side_abstract_mention_links"

    id = Column(Integer, primary_key=True)

    mention_id = Column(
        Integer,
        ForeignKey("sell_side_abstract_mentions.id"),
        nullable=False,
        index=True,
    )
    pubmed_id = Column(
        Integer,
        ForeignKey("pubmed.id"),
        nullable=False,
        index=True,
    )

    # where did this candidate come from?
    match_source = Column(
        String(64),
        nullable=False,
    )  # e.g. "grid_cited", "abstract_number", "url", "title_fuzzy", "context_llm"

    # overall score + feature-level scores
    match_score = Column(Float, nullable=False)
    number_score = Column(Float, nullable=True)
    url_score = Column(Float, nullable=True)
    title_score = Column(Float, nullable=True)
    context_score = Column(Float, nullable=True)
    llm_score = Column(Float, nullable=True)

    is_primary = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
        nullable=False,
    )

    __table_args__ = (
        # you can keep multiple rows per pair (for debugging) or enforce uniqueness:
        # UniqueConstraint("mention_id", "pubmed_id", name="uq_mention_pubmed"),
    )
