from sqlalchemy import Column, DateTime, ForeignKey, String, JSON, Integer, Index, Text, BigInteger
from ...database import Base


class SmartDefGridCellAnswerCitationModel(Base):
    __tablename__ = "smart_def_grid_cell_answer_citations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    answer_id = Column(Integer, ForeignKey("smart_def_grid_cell_answers.id", ondelete="CASCADE"), nullable=False)

    source_type = Column(String(16), nullable=True)  # 'url','doi','patent','pubmed'
    source_id = Column(String(256), nullable=True)   # doi, pubmed id, etc.
    url = Column(Text, nullable=True)
    title = Column(Text, nullable=True)
    snippet = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)
    extra = Column(JSON, nullable=True)

    __table_args__ = (
        Index("ix_smart_def_grid_cell_answer_citations_source", "source_type", "source_id"),
    )
