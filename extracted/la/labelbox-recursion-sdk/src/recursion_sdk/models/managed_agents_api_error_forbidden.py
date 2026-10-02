from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_api_error_forbidden_code import ManagedAgentsApiErrorForbiddenCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_api_error_forbidden_details import ManagedAgentsApiErrorForbiddenDetails





T = TypeVar("T", bound="ManagedAgentsApiErrorForbidden")



@_attrs_define
class ManagedAgentsApiErrorForbidden:
    """ Standard flat error response emitted by a Managed Agents gateway.

        Attributes:
            code (ManagedAgentsApiErrorForbiddenCode): Stable machine-readable error code.
            message (str): Human-readable error message.
            details (ManagedAgentsApiErrorForbiddenDetails | Unset): Optional structured error details.
     """

    code: ManagedAgentsApiErrorForbiddenCode
    message: str
    details: ManagedAgentsApiErrorForbiddenDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_api_error_forbidden_details import ManagedAgentsApiErrorForbiddenDetails # noqa: PLC0415
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
        from ..models.managed_agents_api_error_forbidden_details import ManagedAgentsApiErrorForbiddenDetails # noqa: PLC0415
        d = dict(src_dict)
        code = ManagedAgentsApiErrorForbiddenCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: ManagedAgentsApiErrorForbiddenDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = ManagedAgentsApiErrorForbiddenDetails.from_dict(_details)




        managed_agents_api_error_forbidden = cls(
            code=code,
            message=message,
            details=details,
        )

        return managed_agents_api_error_forbidden

