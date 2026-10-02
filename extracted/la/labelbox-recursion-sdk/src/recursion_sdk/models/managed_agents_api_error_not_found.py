from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_api_error_not_found_code import ManagedAgentsApiErrorNotFoundCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_api_error_not_found_details import ManagedAgentsApiErrorNotFoundDetails





T = TypeVar("T", bound="ManagedAgentsApiErrorNotFound")



@_attrs_define
class ManagedAgentsApiErrorNotFound:
    """ Standard flat error response emitted by a Managed Agents gateway.

        Attributes:
            code (ManagedAgentsApiErrorNotFoundCode): Stable machine-readable error code.
            message (str): Human-readable error message.
            details (ManagedAgentsApiErrorNotFoundDetails | Unset): Optional structured error details.
     """

    code: ManagedAgentsApiErrorNotFoundCode
    message: str
    details: ManagedAgentsApiErrorNotFoundDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_api_error_not_found_details import ManagedAgentsApiErrorNotFoundDetails # noqa: PLC0415
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
        from ..models.managed_agents_api_error_not_found_details import ManagedAgentsApiErrorNotFoundDetails # noqa: PLC0415
        d = dict(src_dict)
        code = ManagedAgentsApiErrorNotFoundCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: ManagedAgentsApiErrorNotFoundDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = ManagedAgentsApiErrorNotFoundDetails.from_dict(_details)




        managed_agents_api_error_not_found = cls(
            code=code,
            message=message,
            details=details,
        )

        return managed_agents_api_error_not_found

