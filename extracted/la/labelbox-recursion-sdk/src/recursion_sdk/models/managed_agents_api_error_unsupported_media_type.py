from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_api_error_unsupported_media_type_code import ManagedAgentsApiErrorUnsupportedMediaTypeCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_api_error_unsupported_media_type_details import ManagedAgentsApiErrorUnsupportedMediaTypeDetails





T = TypeVar("T", bound="ManagedAgentsApiErrorUnsupportedMediaType")



@_attrs_define
class ManagedAgentsApiErrorUnsupportedMediaType:
    """ Standard flat error response emitted by a Managed Agents gateway.

        Attributes:
            code (ManagedAgentsApiErrorUnsupportedMediaTypeCode): Stable machine-readable error code.
            message (str): Human-readable error message.
            details (ManagedAgentsApiErrorUnsupportedMediaTypeDetails | Unset): Optional structured error details.
     """

    code: ManagedAgentsApiErrorUnsupportedMediaTypeCode
    message: str
    details: ManagedAgentsApiErrorUnsupportedMediaTypeDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_api_error_unsupported_media_type_details import ManagedAgentsApiErrorUnsupportedMediaTypeDetails # noqa: PLC0415
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
        from ..models.managed_agents_api_error_unsupported_media_type_details import ManagedAgentsApiErrorUnsupportedMediaTypeDetails # noqa: PLC0415
        d = dict(src_dict)
        code = ManagedAgentsApiErrorUnsupportedMediaTypeCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: ManagedAgentsApiErrorUnsupportedMediaTypeDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = ManagedAgentsApiErrorUnsupportedMediaTypeDetails.from_dict(_details)




        managed_agents_api_error_unsupported_media_type = cls(
            code=code,
            message=message,
            details=details,
        )

        return managed_agents_api_error_unsupported_media_type

