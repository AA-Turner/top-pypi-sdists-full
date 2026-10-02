from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsAutomationDefinitionRunErrorResponse")



@_attrs_define
class ManagedAgentsAutomationDefinitionRunErrorResponse:
    """ Terminal failure that stopped a canonical automation run before or during session admission.

        Example:
            {'code': 'example', 'field': 'example', 'message': 'example', 'resourceId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'retryable': True}

        Attributes:
            code (str): Stable machine-readable failure code.
            message (str): Human-readable failure detail safe to show an operator.
            retryable (bool): Whether another admission may succeed without a configuration change.
            field (str | Unset): Automation field responsible for the failure, when applicable.
            resource_id (UUID | Unset): Referenced resource responsible for the failure, when applicable.
     """

    code: str
    message: str
    retryable: bool
    field: str | Unset = UNSET
    resource_id: UUID | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        retryable = self.retryable

        field = self.field

        resource_id: str | Unset = UNSET
        if not isinstance(self.resource_id, Unset):
            resource_id = str(self.resource_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "code": code,
            "message": message,
            "retryable": retryable,
        })
        if field is not UNSET:
            field_dict["field"] = field
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        retryable = d.pop("retryable")

        field = d.pop("field", UNSET)

        _resource_id = d.pop("resourceId", UNSET)
        resource_id: UUID | Unset
        if isinstance(_resource_id,  Unset):
            resource_id = UNSET
        else:
            resource_id = UUID(_resource_id)




        managed_agents_automation_definition_run_error_response = cls(
            code=code,
            message=message,
            retryable=retryable,
            field=field,
            resource_id=resource_id,
        )

        return managed_agents_automation_definition_run_error_response

