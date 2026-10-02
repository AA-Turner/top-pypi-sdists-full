from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.compute_active_lease_limit_reached_body_dto_code import ComputeActiveLeaseLimitReachedBodyDtoCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.compute_active_lease_limit_reached_body_dto_details import ComputeActiveLeaseLimitReachedBodyDtoDetails





T = TypeVar("T", bound="ComputeActiveLeaseLimitReachedBodyDto")



@_attrs_define
class ComputeActiveLeaseLimitReachedBodyDto:
    """ The caller already holds the maximum number of active leased computes.

        Attributes:
            code (ComputeActiveLeaseLimitReachedBodyDtoCode): Stable machine-readable error code.
            message (str): Human-readable error message.
            details (ComputeActiveLeaseLimitReachedBodyDtoDetails | Unset): Optional structured details. Validation failures
                expose their field-level issues under `details.issues`.
     """

    code: ComputeActiveLeaseLimitReachedBodyDtoCode
    message: str
    details: ComputeActiveLeaseLimitReachedBodyDtoDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.compute_active_lease_limit_reached_body_dto_details import ComputeActiveLeaseLimitReachedBodyDtoDetails # noqa: PLC0415
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
        from ..models.compute_active_lease_limit_reached_body_dto_details import ComputeActiveLeaseLimitReachedBodyDtoDetails # noqa: PLC0415
        d = dict(src_dict)
        code = ComputeActiveLeaseLimitReachedBodyDtoCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: ComputeActiveLeaseLimitReachedBodyDtoDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = ComputeActiveLeaseLimitReachedBodyDtoDetails.from_dict(_details)




        compute_active_lease_limit_reached_body_dto = cls(
            code=code,
            message=message,
            details=details,
        )

        return compute_active_lease_limit_reached_body_dto

