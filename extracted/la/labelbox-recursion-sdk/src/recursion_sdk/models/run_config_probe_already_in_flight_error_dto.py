from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_probe_already_in_flight_error_dto_code import RunConfigProbeAlreadyInFlightErrorDtoCode
from typing import cast

if TYPE_CHECKING:
  from ..models.run_config_probe_already_in_flight_error_dto_details import RunConfigProbeAlreadyInFlightErrorDtoDetails





T = TypeVar("T", bound="RunConfigProbeAlreadyInFlightErrorDto")



@_attrs_define
class RunConfigProbeAlreadyInFlightErrorDto:
    """ Conflict returned when the run-config version already has a pending or running probe.

        Example:
            {'code': 'run_config_probe_already_in_flight', 'message': 'A probe-run is already in flight for this version.
                Resume polling the existing attempt.', 'details': {'existingProbeRunId':
                '1be7d569-e271-4926-af2c-569798de74d7'}}

        Attributes:
            code (RunConfigProbeAlreadyInFlightErrorDtoCode): Machine-readable discriminator for a duplicate in-flight probe
                request.
            message (str): Human-readable explanation that the existing probe should be resumed.
            details (RunConfigProbeAlreadyInFlightErrorDtoDetails): Reference to the in-flight probe-run that already owns
                this attempt.
     """

    code: RunConfigProbeAlreadyInFlightErrorDtoCode
    message: str
    details: RunConfigProbeAlreadyInFlightErrorDtoDetails





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_config_probe_already_in_flight_error_dto_details import RunConfigProbeAlreadyInFlightErrorDtoDetails # noqa: PLC0415
        code = self.code.value

        message = self.message

        details = self.details.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "code": code,
            "message": message,
            "details": details,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_config_probe_already_in_flight_error_dto_details import RunConfigProbeAlreadyInFlightErrorDtoDetails # noqa: PLC0415
        d = dict(src_dict)
        code = RunConfigProbeAlreadyInFlightErrorDtoCode(d.pop("code"))




        message = d.pop("message")

        details = RunConfigProbeAlreadyInFlightErrorDtoDetails.from_dict(d.pop("details"))




        run_config_probe_already_in_flight_error_dto = cls(
            code=code,
            message=message,
            details=details,
        )

        return run_config_probe_already_in_flight_error_dto

