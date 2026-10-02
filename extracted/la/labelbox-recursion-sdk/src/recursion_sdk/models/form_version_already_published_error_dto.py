from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.form_version_already_published_error_dto_code import FormVersionAlreadyPublishedErrorDtoCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.form_version_already_published_error_dto_details import FormVersionAlreadyPublishedErrorDtoDetails





T = TypeVar("T", bound="FormVersionAlreadyPublishedErrorDto")



@_attrs_define
class FormVersionAlreadyPublishedErrorDto:
    """ Conflict returned when an operation requires a draft form version.

        Attributes:
            code (FormVersionAlreadyPublishedErrorDtoCode): Machine-readable discriminator for an already-published form
                version.
            message (str): Human-readable explanation that the form version is already published.
            details (FormVersionAlreadyPublishedErrorDtoDetails | Unset): Optional structured context about the already-
                published form version.
     """

    code: FormVersionAlreadyPublishedErrorDtoCode
    message: str
    details: FormVersionAlreadyPublishedErrorDtoDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_version_already_published_error_dto_details import FormVersionAlreadyPublishedErrorDtoDetails # noqa: PLC0415
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
        from ..models.form_version_already_published_error_dto_details import FormVersionAlreadyPublishedErrorDtoDetails # noqa: PLC0415
        d = dict(src_dict)
        code = FormVersionAlreadyPublishedErrorDtoCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: FormVersionAlreadyPublishedErrorDtoDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = FormVersionAlreadyPublishedErrorDtoDetails.from_dict(_details)




        form_version_already_published_error_dto = cls(
            code=code,
            message=message,
            details=details,
        )

        return form_version_already_published_error_dto

