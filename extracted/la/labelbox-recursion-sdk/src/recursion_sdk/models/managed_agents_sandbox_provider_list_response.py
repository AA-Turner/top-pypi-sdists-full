from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_sandbox_provider import ManagedAgentsSandboxProvider
  from ..models.managed_agents_sandbox_provider_response import ManagedAgentsSandboxProviderResponse





T = TypeVar("T", bound="ManagedAgentsSandboxProviderListResponse")



@_attrs_define
class ManagedAgentsSandboxProviderListResponse:
    """ Response body of GET /v1/sandbox-providers. The only list here that describes the service's own capabilities rather
    than the caller's data: it needs no storage read and returns the same answer for every organization. Whether a
    listed provider is actually usable right now is a separate check, GET /v1/sandbox-providers/{provider}/status.

        Example:
            {'items': [{'default': True, 'description': 'example', 'displayName': 'example', 'provider': 'example',
                'requiresCredential': 'example'}]}

        Attributes:
            items (list[ManagedAgentsSandboxProviderResponse]): Every sandbox provider this build supports. Always an array
                and never null; the compiled-in set does not vary by organization.
            sandbox_providers (list[ManagedAgentsSandboxProvider] | Unset): Deprecated compatibility alias for items. It
                retains snake_case provider fields for older browser clients during rollout.
     """

    items: list[ManagedAgentsSandboxProviderResponse]
    sandbox_providers: list[ManagedAgentsSandboxProvider] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_sandbox_provider import ManagedAgentsSandboxProvider # noqa: PLC0415
        from ..models.managed_agents_sandbox_provider_response import ManagedAgentsSandboxProviderResponse # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        sandbox_providers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sandbox_providers, Unset):
            sandbox_providers = []
            for sandbox_providers_item_data in self.sandbox_providers:
                sandbox_providers_item = sandbox_providers_item_data.to_dict()
                sandbox_providers.append(sandbox_providers_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
        })
        if sandbox_providers is not UNSET:
            field_dict["sandbox_providers"] = sandbox_providers

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_sandbox_provider import ManagedAgentsSandboxProvider # noqa: PLC0415
        from ..models.managed_agents_sandbox_provider_response import ManagedAgentsSandboxProviderResponse # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = ManagedAgentsSandboxProviderResponse.from_dict(items_item_data)



            items.append(items_item)


        _sandbox_providers = d.pop("sandbox_providers", UNSET)
        sandbox_providers: list[ManagedAgentsSandboxProvider] | Unset = UNSET
        if _sandbox_providers is not UNSET:
            sandbox_providers = []
            for sandbox_providers_item_data in _sandbox_providers:
                sandbox_providers_item = ManagedAgentsSandboxProvider.from_dict(sandbox_providers_item_data)



                sandbox_providers.append(sandbox_providers_item)


        managed_agents_sandbox_provider_list_response = cls(
            items=items,
            sandbox_providers=sandbox_providers,
        )

        return managed_agents_sandbox_provider_list_response

