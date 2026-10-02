from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.api_error_status_409_code import ApiErrorStatus409Code
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.api_error_status_409_details import ApiErrorStatus409Details





T = TypeVar("T", bound="ApiErrorStatus409")



@_attrs_define
class ApiErrorStatus409:
    """ Standard flat error response body emitted by the platform exception filter. `code` is the stable machine-readable
    discriminant.

        Attributes:
            code (ApiErrorStatus409Code): Stable machine-readable error code.
            message (str): Human-readable error message.
            details (ApiErrorStatus409Details | Unset): Optional structured details. Validation failures expose their field-
                level issues under `details.issues`.
     """

    code: ApiErrorStatus409Code
    message: str
    details: ApiErrorStatus409Details | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.api_error_status_409_details import ApiErrorStatus409Details # noqa: PLC0415
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
        from ..models.api_error_status_409_details import ApiErrorStatus409Details # noqa: PLC0415
        d = dict(src_dict)
        code = ApiErrorStatus409Code(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: ApiErrorStatus409Details | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = ApiErrorStatus409Details.from_dict(_details)




        api_error_status_409 = cls(
            code=code,
            message=message,
            details=details,
        )

        return api_error_status_409

