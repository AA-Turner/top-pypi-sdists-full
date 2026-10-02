from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.form_version_not_published_error_dto_code import FormVersionNotPublishedErrorDtoCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.form_version_not_published_error_dto_details import FormVersionNotPublishedErrorDtoDetails





T = TypeVar("T", bound="FormVersionNotPublishedErrorDto")



@_attrs_define
class FormVersionNotPublishedErrorDto:
    """ Conflict returned when answers target a form version that is not published.

        Attributes:
            code (FormVersionNotPublishedErrorDtoCode): Machine-readable discriminator for an unpublished form version.
            message (str): Human-readable explanation that answers require a published form version.
            details (FormVersionNotPublishedErrorDtoDetails | Unset): Optional structured context about the unpublished form
                version.
     """

    code: FormVersionNotPublishedErrorDtoCode
    message: str
    details: FormVersionNotPublishedErrorDtoDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_version_not_published_error_dto_details import FormVersionNotPublishedErrorDtoDetails # noqa: PLC0415
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
        from ..models.form_version_not_published_error_dto_details import FormVersionNotPublishedErrorDtoDetails # noqa: PLC0415
        d = dict(src_dict)
        code = FormVersionNotPublishedErrorDtoCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: FormVersionNotPublishedErrorDtoDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = FormVersionNotPublishedErrorDtoDetails.from_dict(_details)




        form_version_not_published_error_dto = cls(
            code=code,
            message=message,
            details=details,
        )

        return form_version_not_published_error_dto

