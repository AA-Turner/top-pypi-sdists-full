from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.health_ok_response_dto_db_status import HealthOkResponseDtoDbStatus






T = TypeVar("T", bound="HealthOkResponseDtoDb")



@_attrs_define
class HealthOkResponseDtoDb:
    """ Database connectivity probe result.

        Attributes:
            status (HealthOkResponseDtoDbStatus): Constant literal indicating the database is reachable.
            latency_ms (float): Round-trip latency of the database health probe, in milliseconds.
     """

    status: HealthOkResponseDtoDbStatus
    latency_ms: float





    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        latency_ms = self.latency_ms


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
            "latencyMs": latency_ms,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = HealthOkResponseDtoDbStatus(d.pop("status"))




        latency_ms = d.pop("latencyMs")

        health_ok_response_dto_db = cls(
            status=status,
            latency_ms=latency_ms,
        )

        return health_ok_response_dto_db

