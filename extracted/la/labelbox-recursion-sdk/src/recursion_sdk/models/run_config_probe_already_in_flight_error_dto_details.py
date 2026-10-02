from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="RunConfigProbeAlreadyInFlightErrorDtoDetails")



@_attrs_define
class RunConfigProbeAlreadyInFlightErrorDtoDetails:
    """ Reference to the in-flight probe-run that already owns this attempt.

        Attributes:
            existing_probe_run_id (UUID): Identifier of the in-flight probe-run the caller should resume polling.
     """

    existing_probe_run_id: UUID





    def to_dict(self) -> dict[str, Any]:
        existing_probe_run_id = str(self.existing_probe_run_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "existingProbeRunId": existing_probe_run_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        existing_probe_run_id = UUID(d.pop("existingProbeRunId"))




        run_config_probe_already_in_flight_error_dto_details = cls(
            existing_probe_run_id=existing_probe_run_id,
        )

        return run_config_probe_already_in_flight_error_dto_details

