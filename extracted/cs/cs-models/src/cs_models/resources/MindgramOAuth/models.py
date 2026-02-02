from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
    Text,
)

from ...database import Base


class MindgramOAuthTokenModel(Base):
    __tablename__ = "mindgram_oauth_tokens"
    __table_args__ = (UniqueConstraint("user_id", "provider", name="ux_user_provider"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(128), nullable=False)
    provider = Column(String(32), nullable=False)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=False)
    token_type = Column(String(32), nullable=True, default="Bearer")
    scope = Column(Text, nullable=True)
    expiry = Column(DateTime, nullable=True)
    token_uri = Column(String(255), nullable=False)
    client_id = Column(String(255), nullable=False)
    client_secret = Column(String(255), nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
