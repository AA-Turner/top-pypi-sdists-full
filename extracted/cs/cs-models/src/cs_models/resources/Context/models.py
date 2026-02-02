# pylint: disable=unnecessary-lambda
from sqlalchemy import (
    Column,
    String,
    Text,
)

from ...database import Base


class ContextModel(Base):
    __tablename__ = "contexts"

    key = Column(String(64), primary_key=True)
    value = Column(Text, nullable=False)
    artifact_id = Column(String(50), nullable=True)
