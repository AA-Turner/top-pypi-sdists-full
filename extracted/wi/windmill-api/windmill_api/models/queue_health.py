from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="QueueHealth")


@_attrs_define
class QueueHealth:
    """Job queue status

    Attributes:
        pending_jobs (int): Number of pending jobs in the queue
        running_jobs (int): Number of currently running jobs
    """

    pending_jobs: int
    running_jobs: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pending_jobs = self.pending_jobs
        running_jobs = self.running_jobs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pending_jobs": pending_jobs,
                "running_jobs": running_jobs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pending_jobs = d.pop("pending_jobs")

        running_jobs = d.pop("running_jobs")

        queue_health = cls(
            pending_jobs=pending_jobs,
            running_jobs=running_jobs,
        )

        queue_health.additional_properties = d
        return queue_health

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
