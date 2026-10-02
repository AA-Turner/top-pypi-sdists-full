from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.form_last_version_error_dto_code import FormLastVersionErrorDtoCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.form_last_version_error_dto_details import FormLastVersionErrorDtoDetails





T = TypeVar("T", bound="FormLastVersionErrorDto")



@_attrs_define
class FormLastVersionErrorDto:
    """ Conflict returned when deleting the only remaining version of a form.

        Attributes:
            code (FormLastVersionErrorDtoCode): Machine-readable discriminator for an attempt to delete the final form
                version.
            message (str): Human-readable explanation that the final form version cannot be deleted.
            details (FormLastVersionErrorDtoDetails | Unset): Optional structured context about the form whose final version
                would be deleted.
     """

    code: FormLastVersionErrorDtoCode
    message: str
    details: FormLastVersionErrorDtoDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_last_version_error_dto_details import FormLastVersionErrorDtoDetails # noqa: PLC0415
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
        from ..models.form_last_version_error_dto_details import FormLastVersionErrorDtoDetails # noqa: PLC0415
        d = dict(src_dict)
        code = FormLastVersionErrorDtoCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: FormLastVersionErrorDtoDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = FormLastVersionErrorDtoDetails.from_dict(_details)




        form_last_version_error_dto = cls(
            code=code,
            message=message,
            details=details,
        )

        return form_last_version_error_dto

