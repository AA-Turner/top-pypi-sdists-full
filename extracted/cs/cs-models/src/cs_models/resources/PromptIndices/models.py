from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
)
from datetime import datetime
from ...database import Base


class PromptIndicesModel(Base):
    __tablename__ = 'prompt_indices'

    id = Column(Integer, primary_key=True)
    prompt_index = Column(String(128), nullable=False)
    text = Column(Text, nullable=False)
    metadatas = Column(Text, nullable=False)
    vector = Column(Text, nullable=False)
    search_type = Column(String(50), nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
