from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsNativeIntegration")



@_attrs_define
class ManagedAgentsNativeIntegration:
    """ A native connection and its agent-owned runtime permission and resource policy.

        Example:
            {'connectionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'permission': 'example', 'resources': ['example']}

        Attributes:
            connection_id (UUID): Active native connection in this organization.
            permission (str): Provider permission preset, bounded by the connection's authorization.
            resources (list[str] | Unset): Optional resource subset. Omit to inherit all resources available through the
                connection. An explicit empty list is rejected.
     """

    connection_id: UUID
    permission: str
    resources: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        connection_id = str(self.connection_id)

        permission = self.permission

        resources: list[str] | Unset = UNSET
        if not isinstance(self.resources, Unset):
            resources = self.resources




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "connectionId": connection_id,
            "permission": permission,
        })
        if resources is not UNSET:
            field_dict["resources"] = resources

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connection_id = UUID(d.pop("connectionId"))




        permission = d.pop("permission")

        resources = cast(list[str], d.pop("resources", UNSET))


        managed_agents_native_integration = cls(
            connection_id=connection_id,
            permission=permission,
            resources=resources,
        )


        managed_agents_native_integration.additional_properties = d
        return managed_agents_native_integration

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
