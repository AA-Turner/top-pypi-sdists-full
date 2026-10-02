from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsRegisterIntegrationConnectionRequest")



@_attrs_define
class ManagedAgentsRegisterIntegrationConnectionRequest:
    """ Request body registering an integration connection directly, by naming a principal the caller owns at the provider.
    The organization comes from the authenticated caller, never from the body.

        Example:
            {'external_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'permission': 'example', 'provider': 'example',
                'resources': ['example']}

        Attributes:
            external_id (str): The customer-owned principal to connect, in the provider's own form. For Google Cloud this is
                the email of a user-managed service account (name@project.iam.gserviceaccount.com); for a built-in integration
                (provider merge) it is the vendor's connector slug from the catalog, e.g. sentry.
            provider (str): Integration provider id returned by listIntegrationProviders. The provider must support direct
                registration; one that connects by install redirect is refused with 422.
            permission (str | Unset): For a built-in integration: the permission preset the allow-list is held to, read
                (every selected tool must be classified read-only) or write (any catalog tool; each is stored at its classified
                level). Omit for read. Refused for providers that select permissions at grant time.
            resources (list[str] | Unset): For a built-in integration (provider merge): the vendor tools the organization's
                agents may use, by tool name from the catalog. Required for that provider and refused for every other; an empty
                list is never read as every tool. Stored on the connection as its allow-list; every agent using the vendor
                inherits it.
     """

    external_id: str
    provider: str
    permission: str | Unset = UNSET
    resources: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        external_id = self.external_id

        provider = self.provider

        permission = self.permission

        resources: list[str] | Unset = UNSET
        if not isinstance(self.resources, Unset):
            resources = self.resources




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "external_id": external_id,
            "provider": provider,
        })
        if permission is not UNSET:
            field_dict["permission"] = permission
        if resources is not UNSET:
            field_dict["resources"] = resources

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        external_id = d.pop("external_id")

        provider = d.pop("provider")

        permission = d.pop("permission", UNSET)

        resources = cast(list[str], d.pop("resources", UNSET))


        managed_agents_register_integration_connection_request = cls(
            external_id=external_id,
            provider=provider,
            permission=permission,
            resources=resources,
        )


        managed_agents_register_integration_connection_request.additional_properties = d
        return managed_agents_register_integration_connection_request

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
