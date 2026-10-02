from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_api_error_unauthorized_code import ManagedAgentsApiErrorUnauthorizedCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_api_error_unauthorized_details import ManagedAgentsApiErrorUnauthorizedDetails





T = TypeVar("T", bound="ManagedAgentsApiErrorUnauthorized")



@_attrs_define
class ManagedAgentsApiErrorUnauthorized:
    """ Standard flat error response emitted by a Managed Agents gateway.

        Attributes:
            code (ManagedAgentsApiErrorUnauthorizedCode): Stable machine-readable error code.
            message (str): Human-readable error message.
            details (ManagedAgentsApiErrorUnauthorizedDetails | Unset): Optional structured error details.
     """

    code: ManagedAgentsApiErrorUnauthorizedCode
    message: str
    details: ManagedAgentsApiErrorUnauthorizedDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_api_error_unauthorized_details import ManagedAgentsApiErrorUnauthorizedDetails # noqa: PLC0415
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
        from ..models.managed_agents_api_error_unauthorized_details import ManagedAgentsApiErrorUnauthorizedDetails # noqa: PLC0415
        d = dict(src_dict)
        code = ManagedAgentsApiErrorUnauthorizedCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: ManagedAgentsApiErrorUnauthorizedDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = ManagedAgentsApiErrorUnauthorizedDetails.from_dict(_details)




        managed_agents_api_error_unauthorized = cls(
            code=code,
            message=message,
            details=details,
        )

        return managed_agents_api_error_unauthorized

