from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_accelerator_catalog_entry import ManagedAgentsAcceleratorCatalogEntry
  from ..models.managed_agents_compute_offering import ManagedAgentsComputeOffering





T = TypeVar("T", bound="ManagedAgentsComputeOfferingListResponse")



@_attrs_define
class ManagedAgentsComputeOfferingListResponse:
    """ Response body of GET /v1/compute-offerings. Describes this deployment's compute capability rather than the caller's
    data, so every organization sees the same list. Use CPU offering capacity to size CPU environments. For GPU
    environments, use the catalog to select an exclusive accelerator and understand host placement; sandbox CPU and
    memory limits remain service-owned and can be smaller than the host.

        Example:
            {'accelerator_catalog': [{'display_name': 'example-name', 'name': 'example-name', 'providers':
                [{'capacity_confidence': 'example', 'observed_at': '2026-02-18T09:30:00Z', 'provider': 'example',
                'quota_headroom': 1, 'quota_limit': 1, 'quota_usage': 1, 'recent_launch_at': '2026-02-18T09:30:00Z', 'region':
                'example', 'telemetry_stale': True, 'warm_allocatable_slots': 1}], 'vram_gb': 1}], 'compute_offerings':
                [{'accelerator': {'count': 1, 'name': 'example-name', 'vram_gb': 1}, 'allocatable_cpu_milli': 1,
                'allocatable_memory_mib': 1, 'available_count': 1, 'capacity_confidence': 'example', 'capacity_level':
                'example', 'cluster_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'machine_label': 'example', 'memory_gib': 1.5,
                'observed_at': '2026-02-18T09:30:00Z', 'offering_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'pool': 'example',
                'price_per_hour_usd': 1.5, 'provider': 'example', 'purchase_model': 'example', 'region': 'example',
                'startup_latency_seconds': 1, 'supports_egress_policy': True, 'supports_privileged': True, 'vcpu': 1, 'zone':
                'example'}], 'stale_clusters': ['example'], 'stale_providers': ['example'], 'telemetry_unavailable': True}

        Attributes:
            accelerator_catalog (list[ManagedAgentsAcceleratorCatalogEntry] | None): Stable deployment-configured
                accelerator choices, enriched with optional provider evidence. This list is not filtered by live provider
                availability.
            compute_offerings (list[ManagedAgentsComputeOffering] | None): Live machine-shape telemetry, cheapest first
                within equal capacity. Empty with telemetry_unavailable false means the catalog was read and had nothing
                placeable; empty with it true means the runner could not be read. Neither removes configured accelerator
                choices.
            telemetry_unavailable (bool): True when the agent runner could not be read and this response falls back to
                configured capability: compute_offerings is empty and every accelerator_catalog evidence row is telemetry_stale.
                A deployment with no configured accelerator catalog answers 503 compute_offerings_unavailable instead.
            stale_clusters (list[str] | Unset): Clusters (cluster_id) whose rows came from a cached snapshot because their
                last refresh failed, for providers that report per cluster. Finer-grained than stale_providers: one cluster of a
                provider can be stale while its others are current.
            stale_providers (list[str] | Unset): Providers whose rows came from a cached snapshot because their last refresh
                failed. Their capacity and price are older than the rest of the response; the shapes themselves remain accurate.
     """

    accelerator_catalog: list[ManagedAgentsAcceleratorCatalogEntry] | None
    compute_offerings: list[ManagedAgentsComputeOffering] | None
    telemetry_unavailable: bool
    stale_clusters: list[str] | Unset = UNSET
    stale_providers: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_accelerator_catalog_entry import ManagedAgentsAcceleratorCatalogEntry # noqa: PLC0415
        from ..models.managed_agents_compute_offering import ManagedAgentsComputeOffering # noqa: PLC0415
        accelerator_catalog: list[dict[str, Any]] | None
        if isinstance(self.accelerator_catalog, list):
            accelerator_catalog = []
            for accelerator_catalog_type_0_item_data in self.accelerator_catalog:
                accelerator_catalog_type_0_item = accelerator_catalog_type_0_item_data.to_dict()
                accelerator_catalog.append(accelerator_catalog_type_0_item)


        else:
            accelerator_catalog = self.accelerator_catalog

        compute_offerings: list[dict[str, Any]] | None
        if isinstance(self.compute_offerings, list):
            compute_offerings = []
            for compute_offerings_type_0_item_data in self.compute_offerings:
                compute_offerings_type_0_item = compute_offerings_type_0_item_data.to_dict()
                compute_offerings.append(compute_offerings_type_0_item)


        else:
            compute_offerings = self.compute_offerings

        telemetry_unavailable = self.telemetry_unavailable

        stale_clusters: list[str] | Unset = UNSET
        if not isinstance(self.stale_clusters, Unset):
            stale_clusters = self.stale_clusters



        stale_providers: list[str] | Unset = UNSET
        if not isinstance(self.stale_providers, Unset):
            stale_providers = self.stale_providers




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "accelerator_catalog": accelerator_catalog,
            "compute_offerings": compute_offerings,
            "telemetry_unavailable": telemetry_unavailable,
        })
        if stale_clusters is not UNSET:
            field_dict["stale_clusters"] = stale_clusters
        if stale_providers is not UNSET:
            field_dict["stale_providers"] = stale_providers

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_accelerator_catalog_entry import ManagedAgentsAcceleratorCatalogEntry # noqa: PLC0415
        from ..models.managed_agents_compute_offering import ManagedAgentsComputeOffering # noqa: PLC0415
        d = dict(src_dict)
        def _parse_accelerator_catalog(data: object) -> list[ManagedAgentsAcceleratorCatalogEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                accelerator_catalog_type_0 = []
                _accelerator_catalog_type_0 = data
                for accelerator_catalog_type_0_item_data in (_accelerator_catalog_type_0):
                    accelerator_catalog_type_0_item = ManagedAgentsAcceleratorCatalogEntry.from_dict(accelerator_catalog_type_0_item_data)



                    accelerator_catalog_type_0.append(accelerator_catalog_type_0_item)

                return accelerator_catalog_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAcceleratorCatalogEntry] | None, data)

        accelerator_catalog = _parse_accelerator_catalog(d.pop("accelerator_catalog"))


        def _parse_compute_offerings(data: object) -> list[ManagedAgentsComputeOffering] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                compute_offerings_type_0 = []
                _compute_offerings_type_0 = data
                for compute_offerings_type_0_item_data in (_compute_offerings_type_0):
                    compute_offerings_type_0_item = ManagedAgentsComputeOffering.from_dict(compute_offerings_type_0_item_data)



                    compute_offerings_type_0.append(compute_offerings_type_0_item)

                return compute_offerings_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsComputeOffering] | None, data)

        compute_offerings = _parse_compute_offerings(d.pop("compute_offerings"))


        telemetry_unavailable = d.pop("telemetry_unavailable")

        stale_clusters = cast(list[str], d.pop("stale_clusters", UNSET))


        stale_providers = cast(list[str], d.pop("stale_providers", UNSET))


        managed_agents_compute_offering_list_response = cls(
            accelerator_catalog=accelerator_catalog,
            compute_offerings=compute_offerings,
            telemetry_unavailable=telemetry_unavailable,
            stale_clusters=stale_clusters,
            stale_providers=stale_providers,
        )


        managed_agents_compute_offering_list_response.additional_properties = d
        return managed_agents_compute_offering_list_response

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
