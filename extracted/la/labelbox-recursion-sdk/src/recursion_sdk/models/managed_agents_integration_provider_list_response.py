from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_provider_info import ManagedAgentsProviderInfo





T = TypeVar("T", bound="ManagedAgentsIntegrationProviderListResponse")



@_attrs_define
class ManagedAgentsIntegrationProviderListResponse:
    """ The integration providers this deployment can connect to. Returned by the provider list a console reads before
    offering a connect action.

        Example:
            {'providers': [{'configured': True, 'display_name': 'example-name', 'egress_hosts': ['example'], 'id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'mcp_endpoint': 'example', 'narrows_by_resource': True, 'permissions':
                ['example'], 'preset_fixed_at_authorization': True}]}

        Attributes:
            providers (list[ManagedAgentsProviderInfo] | None): Every integration provider this build supports, configured
                or not. Unconfigured entries are included so a caller can distinguish "not set up in this deployment" from "not
                offered".
     """

    providers: list[ManagedAgentsProviderInfo] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_provider_info import ManagedAgentsProviderInfo # noqa: PLC0415
        providers: list[dict[str, Any]] | None
        if isinstance(self.providers, list):
            providers = []
            for providers_type_0_item_data in self.providers:
                providers_type_0_item = providers_type_0_item_data.to_dict()
                providers.append(providers_type_0_item)


        else:
            providers = self.providers


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "providers": providers,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_provider_info import ManagedAgentsProviderInfo # noqa: PLC0415
        d = dict(src_dict)
        def _parse_providers(data: object) -> list[ManagedAgentsProviderInfo] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                providers_type_0 = []
                _providers_type_0 = data
                for providers_type_0_item_data in (_providers_type_0):
                    providers_type_0_item = ManagedAgentsProviderInfo.from_dict(providers_type_0_item_data)



                    providers_type_0.append(providers_type_0_item)

                return providers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsProviderInfo] | None, data)

        providers = _parse_providers(d.pop("providers"))


        managed_agents_integration_provider_list_response = cls(
            providers=providers,
        )


        managed_agents_integration_provider_list_response.additional_properties = d
        return managed_agents_integration_provider_list_response

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
