from datetime import datetime
from typing import Any
from uuid import uuid4

import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import mapped_column, Mapped, validates

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_sqlalchemy_util import get_string_info_from_declarative_base, BaseDBM


def generate_default_long_id() -> str:
    return (
        f"longid"
        f"{str(uuid4()).replace('-', '')}"
        f"{str(uuid4()).replace('-', '')}"
        f"{str(now_utc_dt().timestamp()).replace('.', '')}"
    )


def make_slug_from_string(string: str) -> str:
    string = string.strip()
    string = string.replace(" ", "-")
    return string


class SimpleDBM(BaseDBM):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        nullable=False,
        primary_key=True,
        autoincrement=True,
        sort_order=-103,
    )
    long_id: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        unique=True,
        insert_default=generate_default_long_id,
        server_default=func.gen_random_uuid(),
        sort_order=-102,
    )
    slug: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        unique=True,
        sort_order=-101,
    )
    creation_dt: Mapped[datetime] = mapped_column(
        sqlalchemy.TIMESTAMP(timezone=True),
        nullable=False,
        index=True,
        insert_default=now_utc_dt,
        server_default=func.now(),
        sort_order=-100,
    )
    extra_data: Mapped[dict[str, Any]] = mapped_column(
        sqlalchemy.JSON,
        nullable=False,
        index=False,
        insert_default={},
        server_default="{}",
        sort_order=1000,
    )

    def __repr__(self) -> str:
        parts = [f"id={self.id}"]
        if self.slug is not None:
            parts.append(f"slug={self.slug}")
        return f"{self.entity_name} ({', '.join(parts)})"

    @validates("slug")
    def _validate_slug(self, key, value, *args, **kwargs):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is empty")
        value = value.strip()
        if " " in value:
            raise ValueError(f"{key=}, {value=}, value contains spaces")
        return value

    @validates("extra_data")
    def _validate_extra_data(self, key, value, *args, **kwargs):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError(f"{key=}, {value=}, value is not dict")
        return value

    @property
    def id_and_long_id(self) -> str:
        return f"{self.id}--{self.long_id}"

    @property
    def entity_name(self) -> str:
        return self.__class__.__name__.removesuffix("DBM")

    # ---SDP---

    @property
    def sdp_id_and_long_id(self) -> str:
        return self.id_and_long_id

    @property
    def sdp_entity_name(self) -> str:
        return self.entity_name


def get_simple_dbm_class() -> type[SimpleDBM]:
    from project.sqlalchemy_db_.sqlalchemy_model import SimpleDBM
    return SimpleDBM


if __name__ == '__main__':
    print(get_string_info_from_declarative_base(get_simple_dbm_class()))
