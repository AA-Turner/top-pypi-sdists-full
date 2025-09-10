import uuid
from datetime import datetime
from typing import Any
from uuid import uuid4

import sqlalchemy.dialects.postgresql
from sqlalchemy import func
from sqlalchemy.orm import mapped_column, Mapped, validates

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_sqlalchemy_util import get_string_info_from_declarative_base, BaseDBM
from arpakitlib.ar_str_util import make_none_if_blank


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


def _make_word_to_plural(word: str):
    if word.endswith(("s", "x", "z", "ch", "sh")):
        return word + "es"

    if len(word) > 1 and word[-1] == "y" and word[-2].lower() not in "aeiou":
        return word[:-1] + "ies"

    return word + "s"


class SimpleDBM(BaseDBM):
    __abstract__ = True

    class ColumnNames:
        id = "id"
        long_id = "long_id"
        uuid = "uuid"
        slug = "slug"
        creation_dt = "creation_dt"
        private_comment = "private_comment"
        detail_data = "detail_data"
        extra_data = "extra_data"

    id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        nullable=False,
        primary_key=True,
        autoincrement=True,
        sort_order=-104,
    )
    long_id: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        unique=True,
        insert_default=generate_default_long_id,
        server_default=func.gen_random_uuid(),
        sort_order=-103,
    )
    uuid: Mapped[sqlalchemy.dialects.postgresql.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        nullable=False,
        unique=True,
        insert_default=uuid.uuid4,
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
    private_comment: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
    )
    detail_data: Mapped[dict[str, Any]] = mapped_column(
        sqlalchemy.JSON,
        nullable=False,
        index=False,
        insert_default={},
        server_default="{}",
        sort_order=1000,
    )
    extra_data: Mapped[dict[str, Any]] = mapped_column(
        sqlalchemy.JSON,
        nullable=False,
        index=False,
        insert_default={},
        server_default="{}",
        sort_order=1001,
    )

    def __repr__(self) -> str:
        parts = [f"id={self.id}"]
        if self.slug is not None:
            parts.append(f"slug={self.slug}")
        return f"{self.entity_name} ({', '.join(parts)})"

    # ---validators---

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

    @validates("private_comment")
    def _validate_private_comment(self, key, value, *args, **kwargs):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is not str")
        value = make_none_if_blank(value.strip())
        return value

    @validates("detail_data")
    def _validate_detail_data(self, key, value, *args, **kwargs):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError(f"{key=}, {value=}, value is not dict")
        return value

    @validates("extra_data")
    def _validate_extra_data(self, key, value, *args, **kwargs):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError(f"{key=}, {value=}, value is not dict")
        return value

    # ---more---

    @property
    def id_and_long_id(self) -> str:
        return f"{self.id}--{self.long_id}"

    @property
    def id_and_long_id_and_uuid(self) -> str:
        return f"{self.id}--{self.long_id}--{str(self.uuid)}"

    @classmethod
    def get_cls_entity_name(cls) -> str:
        return cls.__name__.removesuffix("DBM")

    @classmethod
    def get_cls_entity_name_plural(cls):
        return _make_word_to_plural(word=cls.get_cls_entity_name())

    @property
    def entity_name(self) -> str:
        return self.__class__.__name__.removesuffix("DBM")

    @property
    def entity_name_plural(self) -> str:
        return _make_word_to_plural(word=self.entity_name)

    @property
    def uuid_as_str(self) -> str:
        return str(self.uuid)

    # ---SDP---

    @property
    def sdp_entity_name(self) -> str:
        return self.entity_name

    @property
    def sdp_entity_name_plural(self) -> str:
        return self.entity_name_plural

    @property
    def sdp_id_and_long_id(self) -> str:
        return self.id_and_long_id

    @property
    def sdp_id_and_long_id_and_uuid(self) -> str:
        return self.id_and_long_id_and_uuid


def get_simple_dbm_class() -> type[SimpleDBM]:
    from project.sqlalchemy_db_.sqlalchemy_model import SimpleDBM
    return SimpleDBM


if __name__ == '__main__':
    print(get_string_info_from_declarative_base(get_simple_dbm_class()))
