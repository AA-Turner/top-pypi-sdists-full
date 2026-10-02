from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_file_clash_error_dto_code import RunConfigFileClashErrorDtoCode
from typing import cast

if TYPE_CHECKING:
  from ..models.run_config_file_clash_error_dto_details import RunConfigFileClashErrorDtoDetails





T = TypeVar("T", bound="RunConfigFileClashErrorDto")



@_attrs_define
class RunConfigFileClashErrorDto:
    """ Error returned when run-config file mount paths collide with problem file paths.

        Attributes:
            code (RunConfigFileClashErrorDtoCode): Discriminator marking this as a run-config file mount-path clash error.
            message (str): Human-readable summary of the clash.
            details (RunConfigFileClashErrorDtoDetails): Container mount paths shared by the run-config files and problem
                files.
     """

    code: RunConfigFileClashErrorDtoCode
    message: str
    details: RunConfigFileClashErrorDtoDetails





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_config_file_clash_error_dto_details import RunConfigFileClashErrorDtoDetails # noqa: PLC0415
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
        from ..models.run_config_file_clash_error_dto_details import RunConfigFileClashErrorDtoDetails # noqa: PLC0415
        d = dict(src_dict)
        code = RunConfigFileClashErrorDtoCode(d.pop("code"))




        message = d.pop("message")

        details = RunConfigFileClashErrorDtoDetails.from_dict(d.pop("details"))




        run_config_file_clash_error_dto = cls(
            code=code,
            message=message,
            details=details,
        )

        return run_config_file_clash_error_dto

