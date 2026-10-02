from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_api_error_semantic_validation_failed_code import ManagedAgentsApiErrorSemanticValidationFailedCode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_api_error_semantic_validation_failed_details import ManagedAgentsApiErrorSemanticValidationFailedDetails





T = TypeVar("T", bound="ManagedAgentsApiErrorSemanticValidationFailed")



@_attrs_define
class ManagedAgentsApiErrorSemanticValidationFailed:
    """ Standard flat error response emitted by a Managed Agents gateway.

        Attributes:
            code (ManagedAgentsApiErrorSemanticValidationFailedCode): Stable machine-readable error code.
            message (str): Human-readable error message.
            details (ManagedAgentsApiErrorSemanticValidationFailedDetails | Unset): Optional structured error details.
     """

    code: ManagedAgentsApiErrorSemanticValidationFailedCode
    message: str
    details: ManagedAgentsApiErrorSemanticValidationFailedDetails | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_api_error_semantic_validation_failed_details import ManagedAgentsApiErrorSemanticValidationFailedDetails # noqa: PLC0415
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
        from ..models.managed_agents_api_error_semantic_validation_failed_details import ManagedAgentsApiErrorSemanticValidationFailedDetails # noqa: PLC0415
        d = dict(src_dict)
        code = ManagedAgentsApiErrorSemanticValidationFailedCode(d.pop("code"))




        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: ManagedAgentsApiErrorSemanticValidationFailedDetails | Unset
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = ManagedAgentsApiErrorSemanticValidationFailedDetails.from_dict(_details)




        managed_agents_api_error_semantic_validation_failed = cls(
            code=code,
            message=message,
            details=details,
        )

        return managed_agents_api_error_semantic_validation_failed

