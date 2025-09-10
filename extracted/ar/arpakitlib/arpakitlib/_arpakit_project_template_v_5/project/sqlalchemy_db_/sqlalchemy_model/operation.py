from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, TYPE_CHECKING

import sqlalchemy
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import mapped_column, Mapped, validates

from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_str_util import make_none_if_blank
from project.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM

if TYPE_CHECKING:
    pass


class OperationDBM(SimpleDBM):
    __tablename__ = "operation"

    class Statuses(Enumeration):
        waiting_for_execution = "waiting_for_execution"
        executing = "executing"
        executed_without_error = "executed_without_error"
        executed_with_error = "executed_with_error"
        cancelled = "cancelled"

    class Types(Enumeration):
        healthcheck_ = "healthcheck"
        raise_fake_error_ = "raise_fake_error"

    class Markers(Enumeration):
        pass

    status: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        index=True,
        insert_default=Statuses.waiting_for_execution,
        server_default=Statuses.waiting_for_execution
    )
    type: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        index=True,
        insert_default=Types.healthcheck_
    )
    marker: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        index=True,
    )
    title: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        index=False
    )
    execution_start_dt: Mapped[datetime | None] = mapped_column(
        sqlalchemy.TIMESTAMP(timezone=True),
        nullable=True,
        index=False
    )
    execution_finish_dt: Mapped[datetime | None] = mapped_column(
        sqlalchemy.TIMESTAMP(timezone=True),
        nullable=True,
        index=False
    )
    input_data: Mapped[dict[str, Any]] = mapped_column(
        postgresql.JSON,
        nullable=False,
        index=False,
        insert_default={},
        server_default="{}",
    )
    output_data: Mapped[dict[str, Any]] = mapped_column(
        postgresql.JSON,
        nullable=False,
        index=False,
        insert_default={},
        server_default="{}",
    )
    error_data: Mapped[dict[str, Any]] = mapped_column(
        postgresql.JSON,
        nullable=False,
        index=False,
        insert_default={},
        server_default="{}",
    )

    def __repr__(self) -> str:
        parts = [f"id={self.id}"]
        if self.status is not None:
            parts.append(f"status={self.status}")
        if self.type is not None:
            parts.append(f"type={self.type}")
        return f"{self.entity_name} ({', '.join(parts)})"

    # ---validators---

    @validates("status")
    def _validate_status(self, key, value, *args, **kwargs):
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is not str")
        value = value.strip()
        if not value:
            raise ValueError(f"{key=}, {value=}, value is empty")
        self.Statuses.parse_and_validate_values(value)
        return value

    @validates("type")
    def _validate_type(self, key, value, *args, **kwargs):
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is not str")
        value = value.strip()
        if not value:
            raise ValueError(f"{key=}, {value=}, value is empty")
        return value

    @validates("marker")
    def _validate_marker(self, key, value, *args, **kwargs):
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

    @validates("input_data")
    def _validate_input_data(self, key, value, *args, **kwargs):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError(f"{key=}, {value=}, value is not dict")
        return value

    @validates("output_data")
    def _validate_output_data(self, key, value, *args, **kwargs):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError(f"{key=}, {value=}, value is not dict")
        return value

    @validates("error_data")
    def _validate_error_data(self, key, value, *args, **kwargs):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError(f"{key=}, {value=}, value is not dict")
        return value

    # ---more---

    def raise_if_executed_with_error(self):
        if self.status == self.Statuses.executed_with_error:
            raise Exception(
                f"Operation ({self.id=}, {self.type=}, {self.status=})"
                f" executed with error, error_data={self.error_data}"
            )

    def raise_if_error_data(self):
        if self.error_data:
            raise Exception(
                f"Operation ({self.id=}, {self.type=}, {self.status=})"
                f" has error_data, error_data={self.error_data}"
            )

    @property
    def duration(self) -> timedelta | None:
        if self.execution_start_dt is None or self.execution_finish_dt is None:
            return None
        return self.execution_finish_dt - self.execution_start_dt

    # ---SDP---

    @property
    def sdp_allowed_statuses(self) -> list[str]:
        return self.Statuses.values_list()

    @property
    def sdp_allowed_types(self) -> list[str]:
        return self.Types.values_list()

    @property
    def sdp_allowed_markers(self) -> list[str]:
        return self.Markers.values_list()

    @property
    def sdp_has_input_data(self) -> bool:
        return bool(self.input_data)

    @property
    def sdp_has_output_data(self) -> bool:
        return bool(self.output_data)

    @property
    def sdp_has_error_data(self) -> bool:
        return bool(self.error_data)

    @property
    def sdp_duration(self) -> timedelta | None:
        return self.duration

    @property
    def sdp_duration_as_str(self) -> str | None:
        if self.duration is None:
            return None
        return str(self.duration)

    @property
    def sdp_duration_total_seconds(self) -> float | None:
        if self.duration is None:
            return None
        return self.duration.total_seconds()

    @property
    def sdp_duration_total_minutes(self) -> float | None:
        if self.duration is None:
            return None
        return self.duration.total_seconds() / 60

    @property
    def sdp_duration_total_hours(self) -> float | None:
        if self.duration is None:
            return None
        return self.duration.total_seconds() / 60 / 60
