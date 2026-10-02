from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsEnvironmentPlacement")



@_attrs_define
class ManagedAgentsEnvironmentPlacement:
    """ Where an environment's sandboxes may run, expressed as constraints rather than a named machine. The runtime selects
    a provider that can enforce the environment's access settings.

        Example:
            {'allow_spot': True, 'max_price_per_hour_usd': 1.5, 'min_accelerator_vram_gb': 1, 'providers': ['example'],
                'regions': ['example']}

        Attributes:
            allow_spot (bool | Unset): Let preemptible capacity compete on price. A reclaimed sandbox is failed and
                restarted from its last snapshot rather than resumed in place, so this trades an occasional lost turn for
                markedly cheaper accelerators.
            max_price_per_hour_usd (float | Unset): Reject offerings priced above this per hour. Offerings whose price is
                unknown are never rejected by this, because an unpriced offering is a gap in a provider's catalog rather than an
                expensive machine.
            min_accelerator_vram_gb (int | Unset): Reject offerings whose per-accelerator memory is below this, in vendor-
                quoted gigabytes. Omit unless a workload genuinely needs the larger variant: an H100 and an H200 run the same
                image and the same snapshot, so treating them as interchangeable is what makes capacity findable.
            providers (list[str] | Unset): Restrict placement to these providers, e.g. gke or nebius. Empty permits
                configured providers compatible with the environment's network policy and privileged access. A nonempty Runs
                network_policy requires gke.
            regions (list[str] | Unset): Regions the sandbox may run in, as each provider names them. Empty means anywhere
                the deployment has configured, which is the usual answer: constraining regions constrains capacity, and capacity
                is the reason to place across providers at all.
     """

    allow_spot: bool | Unset = UNSET
    max_price_per_hour_usd: float | Unset = UNSET
    min_accelerator_vram_gb: int | Unset = UNSET
    providers: list[str] | Unset = UNSET
    regions: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        allow_spot = self.allow_spot

        max_price_per_hour_usd = self.max_price_per_hour_usd

        min_accelerator_vram_gb = self.min_accelerator_vram_gb

        providers: list[str] | Unset = UNSET
        if not isinstance(self.providers, Unset):
            providers = self.providers



        regions: list[str] | Unset = UNSET
        if not isinstance(self.regions, Unset):
            regions = self.regions




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if allow_spot is not UNSET:
            field_dict["allow_spot"] = allow_spot
        if max_price_per_hour_usd is not UNSET:
            field_dict["max_price_per_hour_usd"] = max_price_per_hour_usd
        if min_accelerator_vram_gb is not UNSET:
            field_dict["min_accelerator_vram_gb"] = min_accelerator_vram_gb
        if providers is not UNSET:
            field_dict["providers"] = providers
        if regions is not UNSET:
            field_dict["regions"] = regions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        allow_spot = d.pop("allow_spot", UNSET)

        max_price_per_hour_usd = d.pop("max_price_per_hour_usd", UNSET)

        min_accelerator_vram_gb = d.pop("min_accelerator_vram_gb", UNSET)

        providers = cast(list[str], d.pop("providers", UNSET))


        regions = cast(list[str], d.pop("regions", UNSET))


        managed_agents_environment_placement = cls(
            allow_spot=allow_spot,
            max_price_per_hour_usd=max_price_per_hour_usd,
            min_accelerator_vram_gb=min_accelerator_vram_gb,
            providers=providers,
            regions=regions,
        )


        managed_agents_environment_placement.additional_properties = d
        return managed_agents_environment_placement

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
