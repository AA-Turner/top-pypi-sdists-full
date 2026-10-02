from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_file_clash_invalid_request_error_dto_code import RunConfigFileClashInvalidRequestErrorDtoCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.run_config_file_clash_invalid_request_error_dto_details import RunConfigFileClashInvalidRequestErrorDtoDetails





T = TypeVar("T", bound="RunConfigFileClashInvalidRequestErrorDto")



@_attrs_define
class RunConfigFileClashInvalidRequestErrorDto:
    """ Error returned when the submitted run request is invalid.

        Attributes:
            code (RunConfigFileClashInvalidRequestErrorDtoCode): Machine-readable discriminator for a request that failed
                boundary validation.
            message (str): Human-readable explanation of the invalid run request.
            details (RunConfigFileClashInvalidRequestErrorDtoDetails | Unset): Optional structured boundary-validation
                failures for the invalid run request.
     """

    code: RunConfigFileClashInvalidRequestErrorDtoCode
    message: str
    details: RunConfigFileClashInvalidRequestErrorDtoDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_config_file_clash_invalid_request_error_dto_details import RunConfigFileClashInvalidRequestErrorDtoDetails # noqa: PLC0415
        code = self.code.value

        message = self.message

        details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "code": code,
            "message": message,
        })
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_config_file_clash_invalid_request_error_dto_details import RunConfigFileClashInvalidRequestErrorDtoDetails # noqa: PLC0415
        d = dict(src_dict)
        code = RunConfigFileClashInvalidRequestErrorDtoCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: RunConfigFileClashInvalidRequestErrorDtoDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = RunConfigFileClashInvalidRequestErrorDtoDetails.from_dict(_details)




        run_config_file_clash_invalid_request_error_dto = cls(
            code=code,
            message=message,
            details=details,
        )

        return run_config_file_clash_invalid_request_error_dto

