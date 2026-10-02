from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_compute_offering_accelerator import ManagedAgentsComputeOfferingAccelerator





T = TypeVar("T", bound="ManagedAgentsComputeOffering")



@_attrs_define
class ManagedAgentsComputeOffering:
    """ One host machine shape a sandbox could be placed on, with its CPU, memory, accelerator, current capacity, and
    approximate price. Host capacity may exceed the sandbox's container limit. Read-only deployment capability,
    identical for every organization; nothing here provisions or reserves compute.

        Example:
            {'accelerator': {'count': 1, 'name': 'example-name', 'vram_gb': 1}, 'allocatable_cpu_milli': 1,
                'allocatable_memory_mib': 1, 'available_count': 1, 'capacity_confidence': 'example', 'capacity_level':
                'example', 'cluster_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'machine_label': 'example', 'memory_gib': 1.5,
                'observed_at': '2026-02-18T09:30:00Z', 'offering_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'pool': 'example',
                'price_per_hour_usd': 1.5, 'provider': 'example', 'purchase_model': 'example', 'region': 'example',
                'startup_latency_seconds': 1, 'supports_egress_policy': True, 'supports_privileged': True, 'vcpu': 1, 'zone':
                'example'}

        Attributes:
            capacity_confidence (str): How much capacity_level can be trusted: fresh_count is a live count of launchable
                units, advisory is a directional signal with no count, probe_on_launch means capacity is only discoverable by
                attempting a launch.
            capacity_level (str): high, low, none, or unknown. GKE reports unknown because GCP will not say whether a GPU is
                obtainable until a pool tries to scale.
            machine_label (str): Provider's own name for the machine shape, shown so an operator can recognise it in that
                provider's console.
            memory_gib (float): Memory the machine delivers, in GiB. Like vcpu, the machine's real size rather than the
                environment's request.
            offering_id (str): Stable identifier for this shape in this place. Opaque; compare it, do not parse it.
            provider (str): Compute provider that would serve this offering, e.g. gke or nebius. Distinct from an
                environment's sandbox provider, which stays runs regardless of the cloud underneath.
            purchase_model (str): on_demand or preemptible. Preemptible capacity is cheaper and can be reclaimed by the
                provider.
            region (str): Provider region the offering is in.
            supports_egress_policy (bool): Whether an environment with a network_policy can be placed here. An environment
                that sets one is restricted to offerings where this is true.
            vcpu (int): vCPUs the machine delivers. This is the machine's real size, not the environment's cpu_milli
                request, and it is frequently much larger.
            accelerator (ManagedAgentsComputeOfferingAccelerator | Unset): Accelerator attached to a compute offering, named
                the same way across every provider so an environment's accelerator request means one thing everywhere. Example:
                {'count': 1, 'name': 'example-name', 'vram_gb': 1}.
            allocatable_cpu_milli (int | Unset): CPU one pod can request on this offering's node and still schedule, after
                the kubelet's reservation, in millicores. This is a host ceiling, not the GPU sandbox's service-owned CPU limit.
                Omitted by runners that predate it.
            allocatable_memory_mib (int | Unset): Memory one pod can request on this offering's node and still schedule, in
                MiB. This is a host ceiling, not the GPU sandbox's service-owned memory limit. Omitted by runners that predate
                it.
            available_count (int | Unset): Units the provider reports as launchable right now. Present only when
                capacity_confidence is fresh_count; a present 0 means the provider counted and found none, while an absent value
                means no count was measured.
            cluster_id (str | Unset): Kubernetes cluster the offering is a pool of. Omitted by runners that predate multi-
                cluster placement.
            observed_at (datetime.datetime | Unset): When the runner last refreshed this offering's capacity and price.
            pool (str | Unset): Node pool inside the cluster.
            price_per_hour_usd (float | Unset): Approximate price per hour in USD for the host machine at your
                organization's compute rate. Omitted when the deployment has no price configured for this shape; treat an absent
                price as unknown, never as free.
            startup_latency_seconds (int | Unset): Estimated seconds from pod creation to a ready sandbox on this offering;
                a pool that must scale from zero is slower.
            supports_privileged (bool | Unset): Whether a privileged (Docker-in-Docker) sandbox can be placed here.
            zone (str | Unset): Capacity domain inside the region (a GCP zone, a Nebius fabric). Two zones in one region
                routinely disagree about availability.
     """

    capacity_confidence: str
    capacity_level: str
    machine_label: str
    memory_gib: float
    offering_id: str
    provider: str
    purchase_model: str
    region: str
    supports_egress_policy: bool
    vcpu: int
    accelerator: ManagedAgentsComputeOfferingAccelerator | Unset = UNSET
    allocatable_cpu_milli: int | Unset = UNSET
    allocatable_memory_mib: int | Unset = UNSET
    available_count: int | Unset = UNSET
    cluster_id: str | Unset = UNSET
    observed_at: datetime.datetime | Unset = UNSET
    pool: str | Unset = UNSET
    price_per_hour_usd: float | Unset = UNSET
    startup_latency_seconds: int | Unset = UNSET
    supports_privileged: bool | Unset = UNSET
    zone: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_compute_offering_accelerator import ManagedAgentsComputeOfferingAccelerator # noqa: PLC0415
        capacity_confidence = self.capacity_confidence

        capacity_level = self.capacity_level

        machine_label = self.machine_label

        memory_gib = self.memory_gib

        offering_id = self.offering_id

        provider = self.provider

        purchase_model = self.purchase_model

        region = self.region

        supports_egress_policy = self.supports_egress_policy

        vcpu = self.vcpu

        accelerator: dict[str, Any] | Unset = UNSET
        if not isinstance(self.accelerator, Unset):
            accelerator = self.accelerator.to_dict()

        allocatable_cpu_milli = self.allocatable_cpu_milli

        allocatable_memory_mib = self.allocatable_memory_mib

        available_count = self.available_count

        cluster_id = self.cluster_id

        observed_at: str | Unset = UNSET
        if not isinstance(self.observed_at, Unset):
            observed_at = self.observed_at.isoformat()

        pool = self.pool

        price_per_hour_usd = self.price_per_hour_usd

        startup_latency_seconds = self.startup_latency_seconds

        supports_privileged = self.supports_privileged

        zone = self.zone


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "capacity_confidence": capacity_confidence,
            "capacity_level": capacity_level,
            "machine_label": machine_label,
            "memory_gib": memory_gib,
            "offering_id": offering_id,
            "provider": provider,
            "purchase_model": purchase_model,
            "region": region,
            "supports_egress_policy": supports_egress_policy,
            "vcpu": vcpu,
        })
        if accelerator is not UNSET:
            field_dict["accelerator"] = accelerator
        if allocatable_cpu_milli is not UNSET:
            field_dict["allocatable_cpu_milli"] = allocatable_cpu_milli
        if allocatable_memory_mib is not UNSET:
            field_dict["allocatable_memory_mib"] = allocatable_memory_mib
        if available_count is not UNSET:
            field_dict["available_count"] = available_count
        if cluster_id is not UNSET:
            field_dict["cluster_id"] = cluster_id
        if observed_at is not UNSET:
            field_dict["observed_at"] = observed_at
        if pool is not UNSET:
            field_dict["pool"] = pool
        if price_per_hour_usd is not UNSET:
            field_dict["price_per_hour_usd"] = price_per_hour_usd
        if startup_latency_seconds is not UNSET:
            field_dict["startup_latency_seconds"] = startup_latency_seconds
        if supports_privileged is not UNSET:
            field_dict["supports_privileged"] = supports_privileged
        if zone is not UNSET:
            field_dict["zone"] = zone

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_compute_offering_accelerator import ManagedAgentsComputeOfferingAccelerator # noqa: PLC0415
        d = dict(src_dict)
        capacity_confidence = d.pop("capacity_confidence")

        capacity_level = d.pop("capacity_level")

        machine_label = d.pop("machine_label")

        memory_gib = d.pop("memory_gib")

        offering_id = d.pop("offering_id")

        provider = d.pop("provider")

        purchase_model = d.pop("purchase_model")

        region = d.pop("region")

        supports_egress_policy = d.pop("supports_egress_policy")

        vcpu = d.pop("vcpu")

        _accelerator = d.pop("accelerator", UNSET)
        accelerator: ManagedAgentsComputeOfferingAccelerator | Unset
        if isinstance(_accelerator,  Unset):
            accelerator = UNSET
        else:
            accelerator = ManagedAgentsComputeOfferingAccelerator.from_dict(_accelerator)




        allocatable_cpu_milli = d.pop("allocatable_cpu_milli", UNSET)

        allocatable_memory_mib = d.pop("allocatable_memory_mib", UNSET)

        available_count = d.pop("available_count", UNSET)

        cluster_id = d.pop("cluster_id", UNSET)

        _observed_at = d.pop("observed_at", UNSET)
        observed_at: datetime.datetime | Unset
        if isinstance(_observed_at,  Unset):
            observed_at = UNSET
        else:
            observed_at = datetime.datetime.fromisoformat(_observed_at)




        pool = d.pop("pool", UNSET)

        price_per_hour_usd = d.pop("price_per_hour_usd", UNSET)

        startup_latency_seconds = d.pop("startup_latency_seconds", UNSET)

        supports_privileged = d.pop("supports_privileged", UNSET)

        zone = d.pop("zone", UNSET)

        managed_agents_compute_offering = cls(
            capacity_confidence=capacity_confidence,
            capacity_level=capacity_level,
            machine_label=machine_label,
            memory_gib=memory_gib,
            offering_id=offering_id,
            provider=provider,
            purchase_model=purchase_model,
            region=region,
            supports_egress_policy=supports_egress_policy,
            vcpu=vcpu,
            accelerator=accelerator,
            allocatable_cpu_milli=allocatable_cpu_milli,
            allocatable_memory_mib=allocatable_memory_mib,
            available_count=available_count,
            cluster_id=cluster_id,
            observed_at=observed_at,
            pool=pool,
            price_per_hour_usd=price_per_hour_usd,
            startup_latency_seconds=startup_latency_seconds,
            supports_privileged=supports_privileged,
            zone=zone,
        )


        managed_agents_compute_offering.additional_properties = d
        return managed_agents_compute_offering

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
