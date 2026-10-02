from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsComputeOfferingAccelerator")



@_attrs_define
class ManagedAgentsComputeOfferingAccelerator:
    """ Accelerator attached to a compute offering, named the same way across every provider so an environment's accelerator
    request means one thing everywhere.

        Example:
            {'count': 1, 'name': 'example-name', 'vram_gb': 1}

        Attributes:
            count (int): Number of accelerators attached to one instance of this offering.
            name (str): Canonical accelerator model, lower-case and provider-neutral, e.g. h100. Matches the accelerator
                name an environment requests, whichever provider serves it.
            vram_gb (int): Per-accelerator memory in vendor-quoted gigabytes (H100 is 80, H200 is 141), not gibibytes.
     """

    count: int
    name: str
    vram_gb: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        count = self.count

        name = self.name

        vram_gb = self.vram_gb


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "count": count,
            "name": name,
            "vram_gb": vram_gb,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        name = d.pop("name")

        vram_gb = d.pop("vram_gb")

        managed_agents_compute_offering_accelerator = cls(
            count=count,
            name=name,
            vram_gb=vram_gb,
        )


        managed_agents_compute_offering_accelerator.additional_properties = d
        return managed_agents_compute_offering_accelerator

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
