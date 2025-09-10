from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, validates

from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_str_util import make_none_if_blank
from project.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM

if TYPE_CHECKING:
    pass


class StoryLogDBM(SimpleDBM):
    __tablename__ = "story_log"

    class Levels(Enumeration):
        info = "info"
        warning = "warning"
        error = "error"

    class Types(Enumeration):
        error_in_execute_operation = "error_in_execute_operation"
        error_in_api = "error_in_api"
        error_in_tg_bot = "error_in_tg_bot"
        error_in_execute_with_story_log = "error_in_execute_with_story_log"

    level: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        index=True,
        insert_default=Levels.info,
        server_default=Levels.info,
    )
    type: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        index=True,
    )
    title: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        index=False
    )

    def __repr__(self) -> str:
        res = f"{self.entity_name} (id={self.id}, level={self.level}, type{self.type})"
        return res

    @validates("level")
    def _validate_level(self, key, value, *args, **kwargs):
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is not str")
        value = value.strip()
        self.Levels.parse_and_validate_values(value)
        return value

    @validates("type")
    def _validate_type(self, key, value, *args, **kwargs):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is not str")
        value = make_none_if_blank(value.strip())
        return value

    @validates("title")
    def _validate_title(self, key, value, *args, **kwargs):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is not str")
        value = make_none_if_blank(value.strip())
        return value

    # ---more---

    # ---SDP---

    @property
    def sdp_allowed_levels(self) -> list[str]:
        return self.Levels.values_list()

    @property
    def sdp_allowed_types(self) -> list[str]:
        return self.Types.values_list()
