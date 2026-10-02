from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.form_problem_version_locked_error_dto_code import FormProblemVersionLockedErrorDtoCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.form_problem_version_locked_error_dto_details import FormProblemVersionLockedErrorDtoDetails





T = TypeVar("T", bound="FormProblemVersionLockedErrorDto")



@_attrs_define
class FormProblemVersionLockedErrorDto:
    """ Conflict returned when a locked problem version cannot accept form answers.

        Attributes:
            code (FormProblemVersionLockedErrorDtoCode): Machine-readable discriminator for a locked problem version.
            message (str): Human-readable explanation that the locked problem version rejects form answers.
            details (FormProblemVersionLockedErrorDtoDetails | Unset): Optional structured context about the locked problem
                version.
     """

    code: FormProblemVersionLockedErrorDtoCode
    message: str
    details: FormProblemVersionLockedErrorDtoDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_problem_version_locked_error_dto_details import FormProblemVersionLockedErrorDtoDetails # noqa: PLC0415
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
        from ..models.form_problem_version_locked_error_dto_details import FormProblemVersionLockedErrorDtoDetails # noqa: PLC0415
        d = dict(src_dict)
        code = FormProblemVersionLockedErrorDtoCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: FormProblemVersionLockedErrorDtoDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = FormProblemVersionLockedErrorDtoDetails.from_dict(_details)




        form_problem_version_locked_error_dto = cls(
            code=code,
            message=message,
            details=details,
        )

        return form_problem_version_locked_error_dto

