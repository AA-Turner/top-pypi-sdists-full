from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_api_error_managed_agents_unavailable_code import ManagedAgentsApiErrorManagedAgentsUnavailableCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_api_error_managed_agents_unavailable_details import ManagedAgentsApiErrorManagedAgentsUnavailableDetails





T = TypeVar("T", bound="ManagedAgentsApiErrorManagedAgentsUnavailable")



@_attrs_define
class ManagedAgentsApiErrorManagedAgentsUnavailable:
    """ Standard flat error response emitted by a Managed Agents gateway.

        Attributes:
            code (ManagedAgentsApiErrorManagedAgentsUnavailableCode): Stable machine-readable error code.
            message (str): Human-readable error message.
            details (ManagedAgentsApiErrorManagedAgentsUnavailableDetails | Unset): Optional structured error details.
     """

    code: ManagedAgentsApiErrorManagedAgentsUnavailableCode
    message: str
    details: ManagedAgentsApiErrorManagedAgentsUnavailableDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_api_error_managed_agents_unavailable_details import ManagedAgentsApiErrorManagedAgentsUnavailableDetails # noqa: PLC0415
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
        from ..models.managed_agents_api_error_managed_agents_unavailable_details import ManagedAgentsApiErrorManagedAgentsUnavailableDetails # noqa: PLC0415
        d = dict(src_dict)
        code = ManagedAgentsApiErrorManagedAgentsUnavailableCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: ManagedAgentsApiErrorManagedAgentsUnavailableDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = ManagedAgentsApiErrorManagedAgentsUnavailableDetails.from_dict(_details)




        managed_agents_api_error_managed_agents_unavailable = cls(
            code=code,
            message=message,
            details=details,
        )

        return managed_agents_api_error_managed_agents_unavailable

