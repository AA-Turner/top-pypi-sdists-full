"""Shared base mixins for domain models."""

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    """Adds created_at / updated_at to any SQLModel table class."""

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
