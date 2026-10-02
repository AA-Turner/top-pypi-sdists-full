from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.compute_already_active_body_dto_code import ComputeAlreadyActiveBodyDtoCode
from typing import cast

if TYPE_CHECKING:
  from ..models.compute_already_active_body_dto_details import ComputeAlreadyActiveBodyDtoDetails





T = TypeVar("T", bound="ComputeAlreadyActiveBodyDto")



@_attrs_define
class ComputeAlreadyActiveBodyDto:
    """ Conflict returned when the caller already has an active compute in the requested environment.

        Attributes:
            code (ComputeAlreadyActiveBodyDtoCode): Machine-readable error discriminator for the conflict.
            message (str): Human-readable explanation with the recovery action.
            details (ComputeAlreadyActiveBodyDtoDetails): Identifiers clients use to resume or inspect the compute that is
                already active.
     """

    code: ComputeAlreadyActiveBodyDtoCode
    message: str
    details: ComputeAlreadyActiveBodyDtoDetails





    def to_dict(self) -> dict[str, Any]:
        from ..models.compute_already_active_body_dto_details import ComputeAlreadyActiveBodyDtoDetails # noqa: PLC0415
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
        from ..models.compute_already_active_body_dto_details import ComputeAlreadyActiveBodyDtoDetails # noqa: PLC0415
        d = dict(src_dict)
        code = ComputeAlreadyActiveBodyDtoCode(d.pop("code"))




        message = d.pop("message")

        details = ComputeAlreadyActiveBodyDtoDetails.from_dict(d.pop("details"))




        compute_already_active_body_dto = cls(
            code=code,
            message=message,
            details=details,
        )

        return compute_already_active_body_dto

