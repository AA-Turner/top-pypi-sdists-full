from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkersHealth")


@_attrs_define
class WorkersHealth:
    """Workers health status

    Attributes:
        healthy (bool): Whether any workers are active
        active_count (int): Number of active workers (pinged in last 5 minutes)
        worker_groups (List[str]): List of active worker groups
        min_version (str): Minimum required worker version
        versions (List[str]): List of active worker versions
    """

    healthy: bool
    active_count: int
    worker_groups: List[str]
    min_version: str
    versions: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        healthy = self.healthy
        active_count = self.active_count
        worker_groups = self.worker_groups

        min_version = self.min_version
        versions = self.versions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "healthy": healthy,
                "active_count": active_count,
                "worker_groups": worker_groups,
                "min_version": min_version,
                "versions": versions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        healthy = d.pop("healthy")

        active_count = d.pop("active_count")

        worker_groups = cast(List[str], d.pop("worker_groups"))

        min_version = d.pop("min_version")

        versions = cast(List[str], d.pop("versions"))

        workers_health = cls(
            healthy=healthy,
            active_count=active_count,
            worker_groups=worker_groups,
            min_version=min_version,
            versions=versions,
        )

        workers_health.additional_properties = d
        return workers_health

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
