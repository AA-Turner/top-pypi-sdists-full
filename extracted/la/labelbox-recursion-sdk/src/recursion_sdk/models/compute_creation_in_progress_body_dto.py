from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.compute_creation_in_progress_body_dto_code import ComputeCreationInProgressBodyDtoCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.compute_creation_in_progress_body_dto_details import ComputeCreationInProgressBodyDtoDetails





T = TypeVar("T", bound="ComputeCreationInProgressBodyDto")



@_attrs_define
class ComputeCreationInProgressBodyDto:
    """ Compute admission or reservation state changed concurrently; retrying later may succeed.

        Attributes:
            code (ComputeCreationInProgressBodyDtoCode): Stable machine-readable error code.
            message (str): Human-readable error message.
            details (ComputeCreationInProgressBodyDtoDetails | Unset): Optional structured details. Validation failures
                expose their field-level issues under `details.issues`.
     """

    code: ComputeCreationInProgressBodyDtoCode
    message: str
    details: ComputeCreationInProgressBodyDtoDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.compute_creation_in_progress_body_dto_details import ComputeCreationInProgressBodyDtoDetails # noqa: PLC0415
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
        from ..models.compute_creation_in_progress_body_dto_details import ComputeCreationInProgressBodyDtoDetails # noqa: PLC0415
        d = dict(src_dict)
        code = ComputeCreationInProgressBodyDtoCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: ComputeCreationInProgressBodyDtoDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = ComputeCreationInProgressBodyDtoDetails.from_dict(_details)




        compute_creation_in_progress_body_dto = cls(
            code=code,
            message=message,
            details=details,
        )

        return compute_creation_in_progress_body_dto

