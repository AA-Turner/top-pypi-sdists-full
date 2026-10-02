from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsEnvironmentAccelerator")



@_attrs_define
class ManagedAgentsEnvironmentAccelerator:
    """ An accelerator attached to an environment's sandbox compute. Set it only for GPU workloads; omit it and the sandbox
    runs CPU-only. A GPU sandbox receives one exclusive accelerator with service-owned limits of 8,000 millicores (8
    vCPU) and 32,768 MiB (32 GiB) of memory; its host machine may be larger.

        Example:
            {'count': 1, 'name': 'example-name', 'type': 'example'}

        Attributes:
            count (int | Unset): How many accelerators to attach. Defaults to 1; every offering currently carries one.
            name (str | Unset): Accelerator model, lower-case and provider-neutral, e.g. a100. Must name a model in this
                deployment's configured accelerator_catalog. Live compute offerings enrich that catalog but never remove
                configured choices.
            type_ (str | Unset): Accelerator class to attach. Only gpu is accepted.
     """

    count: int | Unset = UNSET
    name: str | Unset = UNSET
    type_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        count = self.count

        name = self.name

        type_ = self.type_


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if count is not UNSET:
            field_dict["count"] = count
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count", UNSET)

        name = d.pop("name", UNSET)

        type_ = d.pop("type", UNSET)

        managed_agents_environment_accelerator = cls(
            count=count,
            name=name,
            type_=type_,
        )


        managed_agents_environment_accelerator.additional_properties = d
        return managed_agents_environment_accelerator

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
