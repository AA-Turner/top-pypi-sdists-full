from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.triggered_job import TriggeredJob


T = TypeVar("T", bound="TriggerJobsResponse")


@_attrs_define
class TriggerJobsResponse:
    """
    Attributes:
        triggered (list['TriggeredJob']): Jobs that were matched and triggered.
    """

    triggered: list["TriggeredJob"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        triggered = []
        for triggered_item_data in self.triggered:
            triggered_item = triggered_item_data.to_dict()
            triggered.append(triggered_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "triggered": triggered,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.triggered_job import TriggeredJob

        d = dict(src_dict)
        triggered = []
        _triggered = d.pop("triggered")
        for triggered_item_data in _triggered:
            triggered_item = TriggeredJob.from_dict(triggered_item_data)

            triggered.append(triggered_item)

        trigger_jobs_response = cls(
            triggered=triggered,
        )

        trigger_jobs_response.additional_properties = d
        return trigger_jobs_response

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
