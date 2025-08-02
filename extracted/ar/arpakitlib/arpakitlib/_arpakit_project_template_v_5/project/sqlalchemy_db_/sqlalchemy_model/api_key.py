from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, validates

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_str_util import make_none_if_blank
from project.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM

if TYPE_CHECKING:
    pass


def generate_default_api_key_value() -> str:
    return (
        f"apikey"
        f"{str(uuid4()).replace('-', '')}"
        f"{str(uuid4()).replace('-', '')}"
        f"{str(now_utc_dt().timestamp()).replace('.', '')}"
    )


class ApiKeyDBM(SimpleDBM):
    __tablename__ = "api_key"

    title: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True
    )
    value: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        unique=True,
        insert_default=generate_default_api_key_value,
    )
    is_active: Mapped[bool] = mapped_column(
        sqlalchemy.Boolean,
        nullable=False,
        index=True,
        insert_default=True,
        server_default="true"
    )

    def __repr__(self) -> str:
        parts = [f"id={self.id}"]
        if self.title is not None:
            parts.append(f"title={self.title}")
        return f"{self.entity_name} ({', '.join(parts)})"

    @validates("title")
    def _validate_title(self, key, value, *args, **kwargs):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is not str")
        value = make_none_if_blank(value.strip())
        return value

    @validates("value")
    def _validate_value(self, key, value, *args, **kwargs):
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is not str")
        value = value.strip()
        if not value:
            raise ValueError(f"{key=}, {value=}, value is empty")
        return value
