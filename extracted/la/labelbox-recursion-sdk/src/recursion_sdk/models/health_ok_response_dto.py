from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.health_ok_response_dto_status import HealthOkResponseDtoStatus
from typing import cast

if TYPE_CHECKING:
  from ..models.health_ok_response_dto_db import HealthOkResponseDtoDb





T = TypeVar("T", bound="HealthOkResponseDto")



@_attrs_define
class HealthOkResponseDto:
    """ Healthy-branch response from the liveness endpoint, returned with HTTP 200.

        Attributes:
            status (HealthOkResponseDtoStatus): Constant literal indicating the service is healthy.
            uptime (float): Process uptime in seconds since the backend started.
            timestamp (str): Timestamp when the health check ran (ISO-8601, UTC).
            db (HealthOkResponseDtoDb): Database connectivity probe result.
     """

    status: HealthOkResponseDtoStatus
    uptime: float
    timestamp: str
    db: HealthOkResponseDtoDb





    def to_dict(self) -> dict[str, Any]:
        from ..models.health_ok_response_dto_db import HealthOkResponseDtoDb # noqa: PLC0415
        status = self.status.value

        uptime = self.uptime

        timestamp = self.timestamp

        db = self.db.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
            "uptime": uptime,
            "timestamp": timestamp,
            "db": db,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.health_ok_response_dto_db import HealthOkResponseDtoDb # noqa: PLC0415
        d = dict(src_dict)
        status = HealthOkResponseDtoStatus(d.pop("status"))




        uptime = d.pop("uptime")

        timestamp = d.pop("timestamp")

        db = HealthOkResponseDtoDb.from_dict(d.pop("db"))




        health_ok_response_dto = cls(
            status=status,
            uptime=uptime,
            timestamp=timestamp,
            db=db,
        )

        return health_ok_response_dto

