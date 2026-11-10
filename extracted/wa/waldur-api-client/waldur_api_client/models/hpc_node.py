from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HpcNode")


@_attrs_define
class HpcNode:
    """
    Attributes:
        name (str):
        partitions (list[str]):
        state (str):
        cpus (int):
        alloc_cpus (Union[None, int]):
        load_percent (Union[None, float]):
        free_memory_mb (Union[None, int]):
        reason (str):
    """

    name: str
    partitions: list[str]
    state: str
    cpus: int
    alloc_cpus: Union[None, int]
    load_percent: Union[None, float]
    free_memory_mb: Union[None, int]
    reason: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        partitions = self.partitions

        state = self.state

        cpus = self.cpus

        alloc_cpus: Union[None, int]
        alloc_cpus = self.alloc_cpus

        load_percent: Union[None, float]
        load_percent = self.load_percent

        free_memory_mb: Union[None, int]
        free_memory_mb = self.free_memory_mb

        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "partitions": partitions,
                "state": state,
                "cpus": cpus,
                "alloc_cpus": alloc_cpus,
                "load_percent": load_percent,
                "free_memory_mb": free_memory_mb,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        partitions = cast(list[str], d.pop("partitions"))

        state = d.pop("state")

        cpus = d.pop("cpus")

        def _parse_alloc_cpus(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        alloc_cpus = _parse_alloc_cpus(d.pop("alloc_cpus"))

        def _parse_load_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        load_percent = _parse_load_percent(d.pop("load_percent"))

        def _parse_free_memory_mb(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        free_memory_mb = _parse_free_memory_mb(d.pop("free_memory_mb"))

        reason = d.pop("reason")

        hpc_node = cls(
            name=name,
            partitions=partitions,
            state=state,
            cpus=cpus,
            alloc_cpus=alloc_cpus,
            load_percent=load_percent,
            free_memory_mb=free_memory_mb,
            reason=reason,
        )

        hpc_node.additional_properties = d
        return hpc_node

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
