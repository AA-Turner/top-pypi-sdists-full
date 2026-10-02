from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsUpdateIntegrationConnectionSelectionRequest")



@_attrs_define
class ManagedAgentsUpdateIntegrationConnectionSelectionRequest:
    """ Request body replacing the tool allow-list of a built-in integration connection. Validated against the vendor
    catalog exactly as at registration; the connection's state is unchanged and sessions pick the new list up at their
    next credential mint.

        Example:
            {'permission': 'example', 'resources': ['example']}

        Attributes:
            resources (list[str] | None): The vendor tools the organization's agents may use, by tool name from the catalog.
                Replaces the connection's allow-list in full; an empty list is refused.
            permission (str | Unset): The permission preset the allow-list is held to: read (every tool must be classified
                read-only) or write (any catalog tool; each is stored at its classified level). Omit for read.
     """

    resources: list[str] | None
    permission: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        resources: list[str] | None
        if isinstance(self.resources, list):
            resources = self.resources


        else:
            resources = self.resources

        permission = self.permission


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "resources": resources,
        })
        if permission is not UNSET:
            field_dict["permission"] = permission

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_resources(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                resources_type_0 = cast(list[str], data)

                return resources_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        resources = _parse_resources(d.pop("resources"))


        permission = d.pop("permission", UNSET)

        managed_agents_update_integration_connection_selection_request = cls(
            resources=resources,
            permission=permission,
        )


        managed_agents_update_integration_connection_selection_request.additional_properties = d
        return managed_agents_update_integration_connection_selection_request

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
