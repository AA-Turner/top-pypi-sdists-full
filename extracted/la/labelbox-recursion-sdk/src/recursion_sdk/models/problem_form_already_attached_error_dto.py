from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_form_already_attached_error_dto_code import ProblemFormAlreadyAttachedErrorDtoCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.problem_form_already_attached_error_dto_details import ProblemFormAlreadyAttachedErrorDtoDetails





T = TypeVar("T", bound="ProblemFormAlreadyAttachedErrorDto")



@_attrs_define
class ProblemFormAlreadyAttachedErrorDto:
    """ Conflict returned when the problem already has a form attached.

        Attributes:
            code (ProblemFormAlreadyAttachedErrorDtoCode): Machine-readable discriminator for a duplicate problem form
                attachment.
            message (str): Human-readable explanation of the duplicate problem form attachment.
            details (ProblemFormAlreadyAttachedErrorDtoDetails | Unset): Optional structured context about the existing
                problem form attachment.
     """

    code: ProblemFormAlreadyAttachedErrorDtoCode
    message: str
    details: ProblemFormAlreadyAttachedErrorDtoDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_form_already_attached_error_dto_details import ProblemFormAlreadyAttachedErrorDtoDetails # noqa: PLC0415
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
        from ..models.problem_form_already_attached_error_dto_details import ProblemFormAlreadyAttachedErrorDtoDetails # noqa: PLC0415
        d = dict(src_dict)
        code = ProblemFormAlreadyAttachedErrorDtoCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: ProblemFormAlreadyAttachedErrorDtoDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = ProblemFormAlreadyAttachedErrorDtoDetails.from_dict(_details)




        problem_form_already_attached_error_dto = cls(
            code=code,
            message=message,
            details=details,
        )

        return problem_form_already_attached_error_dto

