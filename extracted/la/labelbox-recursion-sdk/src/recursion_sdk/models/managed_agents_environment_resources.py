from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_environment_accelerator import ManagedAgentsEnvironmentAccelerator
  from ..models.managed_agents_environment_placement import ManagedAgentsEnvironmentPlacement





T = TypeVar("T", bound="ManagedAgentsEnvironmentResources")



@_attrs_define
class ManagedAgentsEnvironmentResources:
    """ Compute sizing and lifetime for an environment's sandbox. CPU environments accept caller-selected CPU and memory.
    GPU environments accept an exclusive accelerator plus optional lifetime and placement constraints, but use service-
    owned limits of 8,000 millicores (8 vCPU) and 32,768 MiB (32 GiB) of memory.

        Example:
            {'accelerator': {'count': 1, 'name': 'example-name', 'type': 'example'}, 'cpu_milli': 1, 'memory_mib': 1,
                'placement': {'allow_spot': True, 'max_price_per_hour_usd': 1.5, 'min_accelerator_vram_gb': 1, 'providers':
                ['example'], 'regions': ['example']}, 'timeout_seconds': 1}

        Attributes:
            accelerator (ManagedAgentsEnvironmentAccelerator | Unset): An accelerator attached to an environment's sandbox
                compute. Set it only for GPU workloads; omit it and the sandbox runs CPU-only. A GPU sandbox receives one
                exclusive accelerator with service-owned limits of 8,000 millicores (8 vCPU) and 32,768 MiB (32 GiB) of memory;
                its host machine may be larger. Example: {'count': 1, 'name': 'example-name', 'type': 'example'}.
            cpu_milli (int | Unset): CPU request in millicores, so 1000 is one vCPU; 0 uses the provider default. CPU-only
                environments; must be omitted with an accelerator because the GPU sandbox CPU limit is service-owned.
            memory_mib (int | Unset): Memory request in MiB; 0 uses the provider default. CPU-only environments; must be
                omitted with an accelerator because the GPU sandbox memory limit is service-owned.
            placement (ManagedAgentsEnvironmentPlacement | Unset): Where an environment's sandboxes may run, expressed as
                constraints rather than a named machine. The runtime selects a provider that can enforce the environment's
                access settings. Example: {'allow_spot': True, 'max_price_per_hour_usd': 1.5, 'min_accelerator_vram_gb': 1,
                'providers': ['example'], 'regions': ['example']}.
            timeout_seconds (int | Unset): Maximum sandbox lifetime in seconds before the provider tears it down; 0 uses the
                provider default.
     """

    accelerator: ManagedAgentsEnvironmentAccelerator | Unset = UNSET
    cpu_milli: int | Unset = UNSET
    memory_mib: int | Unset = UNSET
    placement: ManagedAgentsEnvironmentPlacement | Unset = UNSET
    timeout_seconds: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_environment_accelerator import ManagedAgentsEnvironmentAccelerator # noqa: PLC0415
        from ..models.managed_agents_environment_placement import ManagedAgentsEnvironmentPlacement # noqa: PLC0415
        accelerator: dict[str, Any] | Unset = UNSET
        if not isinstance(self.accelerator, Unset):
            accelerator = self.accelerator.to_dict()

        cpu_milli = self.cpu_milli

        memory_mib = self.memory_mib

        placement: dict[str, Any] | Unset = UNSET
        if not isinstance(self.placement, Unset):
            placement = self.placement.to_dict()

        timeout_seconds = self.timeout_seconds


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if accelerator is not UNSET:
            field_dict["accelerator"] = accelerator
        if cpu_milli is not UNSET:
            field_dict["cpu_milli"] = cpu_milli
        if memory_mib is not UNSET:
            field_dict["memory_mib"] = memory_mib
        if placement is not UNSET:
            field_dict["placement"] = placement
        if timeout_seconds is not UNSET:
            field_dict["timeout_seconds"] = timeout_seconds

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_environment_accelerator import ManagedAgentsEnvironmentAccelerator # noqa: PLC0415
        from ..models.managed_agents_environment_placement import ManagedAgentsEnvironmentPlacement # noqa: PLC0415
        d = dict(src_dict)
        _accelerator = d.pop("accelerator", UNSET)
        accelerator: ManagedAgentsEnvironmentAccelerator | Unset
        if isinstance(_accelerator,  Unset):
            accelerator = UNSET
        else:
            accelerator = ManagedAgentsEnvironmentAccelerator.from_dict(_accelerator)




        cpu_milli = d.pop("cpu_milli", UNSET)

        memory_mib = d.pop("memory_mib", UNSET)

        _placement = d.pop("placement", UNSET)
        placement: ManagedAgentsEnvironmentPlacement | Unset
        if isinstance(_placement,  Unset):
            placement = UNSET
        else:
            placement = ManagedAgentsEnvironmentPlacement.from_dict(_placement)




        timeout_seconds = d.pop("timeout_seconds", UNSET)

        managed_agents_environment_resources = cls(
            accelerator=accelerator,
            cpu_milli=cpu_milli,
            memory_mib=memory_mib,
            placement=placement,
            timeout_seconds=timeout_seconds,
        )


        managed_agents_environment_resources.additional_properties = d
        return managed_agents_environment_resources

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
