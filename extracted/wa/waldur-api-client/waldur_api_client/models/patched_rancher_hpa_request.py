from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedRancherHPARequest")


@_attrs_define
class PatchedRancherHPARequest:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        workload (Union[None, Unset, str]):
        min_replicas (Union[Unset, int]):
        max_replicas (Union[Unset, int]):
        metrics (Union[Unset, Any]):
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    workload: Union[None, Unset, str] = UNSET
    min_replicas: Union[Unset, int] = UNSET
    max_replicas: Union[Unset, int] = UNSET
    metrics: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        workload: Union[None, Unset, str]
        if isinstance(self.workload, Unset):
            workload = UNSET
        else:
            workload = self.workload

        min_replicas = self.min_replicas

        max_replicas = self.max_replicas

        metrics = self.metrics

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if workload is not UNSET:
            field_dict["workload"] = workload
        if min_replicas is not UNSET:
            field_dict["min_replicas"] = min_replicas
        if max_replicas is not UNSET:
            field_dict["max_replicas"] = max_replicas
        if metrics is not UNSET:
            field_dict["metrics"] = metrics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        def _parse_workload(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        workload = _parse_workload(d.pop("workload", UNSET))

        min_replicas = d.pop("min_replicas", UNSET)

        max_replicas = d.pop("max_replicas", UNSET)

        metrics = d.pop("metrics", UNSET)

        patched_rancher_hpa_request = cls(
            name=name,
            description=description,
            workload=workload,
            min_replicas=min_replicas,
            max_replicas=max_replicas,
            metrics=metrics,
        )

        patched_rancher_hpa_request.additional_properties = d
        return patched_rancher_hpa_request

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
