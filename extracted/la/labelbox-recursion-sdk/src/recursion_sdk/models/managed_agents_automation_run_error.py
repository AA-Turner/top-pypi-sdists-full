from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsAutomationRunError")



@_attrs_define
class ManagedAgentsAutomationRunError:
    """ Why one automation run did not create a session.

        Example:
            {'code': 'example', 'field': 'example', 'message': 'example', 'resource_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'retryable': True}

        Attributes:
            code (str): Stable machine-readable failure code, for example environment_archived or session_rate_limited.
            message (str): Human-readable detail, safe to show an operator.
            retryable (bool): Whether a later run may succeed without a configuration change. Does not imply this run will
                retry. A retryable failure does not pause the automation.
            field (str | Unset): Which piece of the automation's configuration the failure was about, for example
                agent_version_id or vault_ids.
            resource_id (str | Unset): Identifier of the resource that could not be resolved, when the code names one.
     """

    code: str
    message: str
    retryable: bool
    field: str | Unset = UNSET
    resource_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        retryable = self.retryable

        field = self.field

        resource_id = self.resource_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "code": code,
            "message": message,
            "retryable": retryable,
        })
        if field is not UNSET:
            field_dict["field"] = field
        if resource_id is not UNSET:
            field_dict["resource_id"] = resource_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        retryable = d.pop("retryable")

        field = d.pop("field", UNSET)

        resource_id = d.pop("resource_id", UNSET)

        managed_agents_automation_run_error = cls(
            code=code,
            message=message,
            retryable=retryable,
            field=field,
            resource_id=resource_id,
        )


        managed_agents_automation_run_error.additional_properties = d
        return managed_agents_automation_run_error

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
