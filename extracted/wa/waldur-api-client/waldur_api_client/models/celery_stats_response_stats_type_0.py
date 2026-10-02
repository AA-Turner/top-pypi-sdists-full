from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.celery_worker_stats import CeleryWorkerStats


T = TypeVar("T", bound="CeleryStatsResponseStatsType0")


@_attrs_define
class CeleryStatsResponseStatsType0:
    """Detailed statistics per worker including uptime, pool info, and resource usage. Keys are worker names."""

    additional_properties: dict[str, "CeleryWorkerStats"] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.celery_worker_stats import CeleryWorkerStats

        d = dict(src_dict)
        celery_stats_response_stats_type_0 = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = CeleryWorkerStats.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        celery_stats_response_stats_type_0.additional_properties = additional_properties
        return celery_stats_response_stats_type_0

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "CeleryWorkerStats":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "CeleryWorkerStats") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
