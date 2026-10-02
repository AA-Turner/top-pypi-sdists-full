from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsProviderInfo")



@_attrs_define
class ManagedAgentsProviderInfo:
    """ One integration provider this build supports, together with whether this deployment is configured for it. Returned
    by the provider list a console reads before offering a connect action.

        Example:
            {'configured': True, 'display_name': 'example-name', 'egress_hosts': ['example'], 'id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'mcp_endpoint': 'example', 'narrows_by_resource': True, 'permissions':
                ['example'], 'preset_fixed_at_authorization': True}

        Attributes:
            configured (bool): Whether this deployment can start authorization for the provider. Present for clients that
                also consume provider catalogs containing unavailable entries.
            display_name (str): Human-readable provider name for the connect UI, for example "GitHub".
            id (str): Stable provider slug to pass wherever an integration provider is named, such as starting an install.
            egress_hosts (list[str] | Unset): Hostnames a sandbox must be allowed to reach for this provider's in-container
                tooling. Empty when the provider needs no sandbox egress.
            mcp_endpoint (str | Unset): MCP server URL that sessions granted this provider get bound to. Empty only when the
                supported provider exposes no MCP surface.
            narrows_by_resource (bool | Unset): True when a vault grant for this provider may be narrowed to specific
                resources within the connection, and the provider enforces that narrowing when it mints. GitHub (repositories)
                is the only such provider today. False or omitted means integration_resources is rejected, so a grant UI should
                offer no resource picker.
            permissions (list[str] | Unset): Named permission presets a vault grant may request for this supported provider,
                ordered least privileged first.
            preset_fixed_at_authorization (bool | Unset): True when this provider's permission preset is fixed for the life
                of its OAuth grant and cannot be narrowed later at vault-grant time, unlike the common case (e.g. GitHub). The
                connect UI should let the operator choose a preset before starting authorization when this is true; false or
                omitted means the existing post-connect vault-grant preset choice is sufficient.
     """

    configured: bool
    display_name: str
    id: str
    egress_hosts: list[str] | Unset = UNSET
    mcp_endpoint: str | Unset = UNSET
    narrows_by_resource: bool | Unset = UNSET
    permissions: list[str] | Unset = UNSET
    preset_fixed_at_authorization: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        configured = self.configured

        display_name = self.display_name

        id = self.id

        egress_hosts: list[str] | Unset = UNSET
        if not isinstance(self.egress_hosts, Unset):
            egress_hosts = self.egress_hosts



        mcp_endpoint = self.mcp_endpoint

        narrows_by_resource = self.narrows_by_resource

        permissions: list[str] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions



        preset_fixed_at_authorization = self.preset_fixed_at_authorization


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "configured": configured,
            "display_name": display_name,
            "id": id,
        })
        if egress_hosts is not UNSET:
            field_dict["egress_hosts"] = egress_hosts
        if mcp_endpoint is not UNSET:
            field_dict["mcp_endpoint"] = mcp_endpoint
        if narrows_by_resource is not UNSET:
            field_dict["narrows_by_resource"] = narrows_by_resource
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if preset_fixed_at_authorization is not UNSET:
            field_dict["preset_fixed_at_authorization"] = preset_fixed_at_authorization

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        configured = d.pop("configured")

        display_name = d.pop("display_name")

        id = d.pop("id")

        egress_hosts = cast(list[str], d.pop("egress_hosts", UNSET))


        mcp_endpoint = d.pop("mcp_endpoint", UNSET)

        narrows_by_resource = d.pop("narrows_by_resource", UNSET)

        permissions = cast(list[str], d.pop("permissions", UNSET))


        preset_fixed_at_authorization = d.pop("preset_fixed_at_authorization", UNSET)

        managed_agents_provider_info = cls(
            configured=configured,
            display_name=display_name,
            id=id,
            egress_hosts=egress_hosts,
            mcp_endpoint=mcp_endpoint,
            narrows_by_resource=narrows_by_resource,
            permissions=permissions,
            preset_fixed_at_authorization=preset_fixed_at_authorization,
        )


        managed_agents_provider_info.additional_properties = d
        return managed_agents_provider_info

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
