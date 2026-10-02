from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.target_api_error_invariant_violation_code import TargetApiErrorInvariantViolationCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.target_api_error_invariant_violation_details import TargetApiErrorInvariantViolationDetails





T = TypeVar("T", bound="TargetApiErrorInvariantViolation")



@_attrs_define
class TargetApiErrorInvariantViolation:
    """ Standard flat error response body emitted by the platform exception filter. `code` is the stable machine-readable
    discriminant.

        Attributes:
            code (TargetApiErrorInvariantViolationCode): Stable machine-readable error code.
            message (str): Human-readable error message.
            details (TargetApiErrorInvariantViolationDetails | Unset): Optional structured details. Validation failures
                expose their field-level issues under `details.issues`.
     """

    code: TargetApiErrorInvariantViolationCode
    message: str
    details: TargetApiErrorInvariantViolationDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.target_api_error_invariant_violation_details import TargetApiErrorInvariantViolationDetails # noqa: PLC0415
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
        from ..models.target_api_error_invariant_violation_details import TargetApiErrorInvariantViolationDetails # noqa: PLC0415
        d = dict(src_dict)
        code = TargetApiErrorInvariantViolationCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: TargetApiErrorInvariantViolationDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = TargetApiErrorInvariantViolationDetails.from_dict(_details)




        target_api_error_invariant_violation = cls(
            code=code,
            message=message,
            details=details,
        )

        return target_api_error_invariant_violation

