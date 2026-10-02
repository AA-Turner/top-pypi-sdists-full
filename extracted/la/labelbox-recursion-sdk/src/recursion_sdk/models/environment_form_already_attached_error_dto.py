from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.environment_form_already_attached_error_dto_code import EnvironmentFormAlreadyAttachedErrorDtoCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.environment_form_already_attached_error_dto_details import EnvironmentFormAlreadyAttachedErrorDtoDetails





T = TypeVar("T", bound="EnvironmentFormAlreadyAttachedErrorDto")



@_attrs_define
class EnvironmentFormAlreadyAttachedErrorDto:
    """ Conflict returned when the environment already has a form attached.

        Attributes:
            code (EnvironmentFormAlreadyAttachedErrorDtoCode): Machine-readable discriminator for a duplicate environment
                form attachment.
            message (str): Human-readable explanation of the duplicate environment form attachment.
            details (EnvironmentFormAlreadyAttachedErrorDtoDetails | Unset): Optional structured context about the existing
                environment form attachment.
     """

    code: EnvironmentFormAlreadyAttachedErrorDtoCode
    message: str
    details: EnvironmentFormAlreadyAttachedErrorDtoDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.environment_form_already_attached_error_dto_details import EnvironmentFormAlreadyAttachedErrorDtoDetails # noqa: PLC0415
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
        from ..models.environment_form_already_attached_error_dto_details import EnvironmentFormAlreadyAttachedErrorDtoDetails # noqa: PLC0415
        d = dict(src_dict)
        code = EnvironmentFormAlreadyAttachedErrorDtoCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: EnvironmentFormAlreadyAttachedErrorDtoDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = EnvironmentFormAlreadyAttachedErrorDtoDetails.from_dict(_details)




        environment_form_already_attached_error_dto = cls(
            code=code,
            message=message,
            details=details,
        )

        return environment_form_already_attached_error_dto

