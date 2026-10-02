from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_accelerator_provider_evidence import ManagedAgentsAcceleratorProviderEvidence





T = TypeVar("T", bound="ManagedAgentsAcceleratorCatalogEntry")



@_attrs_define
class ManagedAgentsAcceleratorCatalogEntry:
    """ One accelerator model this deployment is configured to offer, listed regardless of live provider availability, with
    whatever provider quota and capacity evidence is currently known. Deployment capability, identical for every
    organization; nothing here provisions or reserves compute.

        Example:
            {'display_name': 'example-name', 'name': 'example-name', 'providers': [{'capacity_confidence': 'example',
                'observed_at': '2026-02-18T09:30:00Z', 'provider': 'example', 'quota_headroom': 1, 'quota_limit': 1,
                'quota_usage': 1, 'recent_launch_at': '2026-02-18T09:30:00Z', 'region': 'example', 'telemetry_stale': True,
                'warm_allocatable_slots': 1}], 'vram_gb': 1}

        Attributes:
            display_name (str): Human-readable model label.
            name (str): Canonical provider-neutral model stored on environments, e.g. a100, l4, or t4.
            providers (list[ManagedAgentsAcceleratorProviderEvidence] | None): Provider evidence; empty means unknown, not
                unavailable.
            vram_gb (int | Unset): Nominal per-accelerator memory in vendor-quoted gigabytes.
     """

    display_name: str
    name: str
    providers: list[ManagedAgentsAcceleratorProviderEvidence] | None
    vram_gb: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_accelerator_provider_evidence import ManagedAgentsAcceleratorProviderEvidence # noqa: PLC0415
        display_name = self.display_name

        name = self.name

        providers: list[dict[str, Any]] | None
        if isinstance(self.providers, list):
            providers = []
            for providers_type_0_item_data in self.providers:
                providers_type_0_item = providers_type_0_item_data.to_dict()
                providers.append(providers_type_0_item)


        else:
            providers = self.providers

        vram_gb = self.vram_gb


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "display_name": display_name,
            "name": name,
            "providers": providers,
        })
        if vram_gb is not UNSET:
            field_dict["vram_gb"] = vram_gb

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_accelerator_provider_evidence import ManagedAgentsAcceleratorProviderEvidence # noqa: PLC0415
        d = dict(src_dict)
        display_name = d.pop("display_name")

        name = d.pop("name")

        def _parse_providers(data: object) -> list[ManagedAgentsAcceleratorProviderEvidence] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                providers_type_0 = []
                _providers_type_0 = data
                for providers_type_0_item_data in (_providers_type_0):
                    providers_type_0_item = ManagedAgentsAcceleratorProviderEvidence.from_dict(providers_type_0_item_data)



                    providers_type_0.append(providers_type_0_item)

                return providers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAcceleratorProviderEvidence] | None, data)

        providers = _parse_providers(d.pop("providers"))


        vram_gb = d.pop("vram_gb", UNSET)

        managed_agents_accelerator_catalog_entry = cls(
            display_name=display_name,
            name=name,
            providers=providers,
            vram_gb=vram_gb,
        )


        managed_agents_accelerator_catalog_entry.additional_properties = d
        return managed_agents_accelerator_catalog_entry

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
