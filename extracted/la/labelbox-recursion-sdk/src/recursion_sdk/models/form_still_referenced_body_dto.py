from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.form_still_referenced_body_dto_code import FormStillReferencedBodyDtoCode
from typing import cast

if TYPE_CHECKING:
  from ..models.form_still_referenced_body_dto_details import FormStillReferencedBodyDtoDetails





T = TypeVar("T", bound="FormStillReferencedBodyDto")



@_attrs_define
class FormStillReferencedBodyDto:
    """ Conflict returned when environment or problem attachments still reference the form.

        Attributes:
            code (FormStillReferencedBodyDtoCode): Machine-readable error discriminator for the conflict.
            message (str): Human-readable explanation with the recovery action.
            details (FormStillReferencedBodyDtoDetails): Environment and problem identifiers that must release the form
                before it can be detached.
     """

    code: FormStillReferencedBodyDtoCode
    message: str
    details: FormStillReferencedBodyDtoDetails





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_still_referenced_body_dto_details import FormStillReferencedBodyDtoDetails # noqa: PLC0415
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
        from ..models.form_still_referenced_body_dto_details import FormStillReferencedBodyDtoDetails # noqa: PLC0415
        d = dict(src_dict)
        code = FormStillReferencedBodyDtoCode(d.pop("code"))




        message = d.pop("message")

        details = FormStillReferencedBodyDtoDetails.from_dict(d.pop("details"))




        form_still_referenced_body_dto = cls(
            code=code,
            message=message,
            details=details,
        )

        return form_still_referenced_body_dto

