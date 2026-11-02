import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtendedJobsJobsItemType1WorkflowAsCodeStatus")


@_attrs_define
class ExtendedJobsJobsItemType1WorkflowAsCodeStatus:
    """
    Attributes:
        scheduled_for (Union[Unset, datetime.datetime]):
        started_at (Union[Unset, datetime.datetime]):
        duration_ms (Union[Unset, float]):
        name (Union[Unset, str]):
    """

    scheduled_for: Union[Unset, datetime.datetime] = UNSET
    started_at: Union[Unset, datetime.datetime] = UNSET
    duration_ms: Union[Unset, float] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scheduled_for: Union[Unset, str] = UNSET
        if not isinstance(self.scheduled_for, Unset):
            scheduled_for = self.scheduled_for.isoformat()

        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        duration_ms = self.duration_ms
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scheduled_for is not UNSET:
            field_dict["scheduled_for"] = scheduled_for
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _scheduled_for = d.pop("scheduled_for", UNSET)
        scheduled_for: Union[Unset, datetime.datetime]
        if isinstance(_scheduled_for, Unset):
            scheduled_for = UNSET
        else:
            scheduled_for = isoparse(_scheduled_for)

        _started_at = d.pop("started_at", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        duration_ms = d.pop("duration_ms", UNSET)

        name = d.pop("name", UNSET)

        extended_jobs_jobs_item_type_1_workflow_as_code_status = cls(
            scheduled_for=scheduled_for,
            started_at=started_at,
            duration_ms=duration_ms,
            name=name,
        )

        extended_jobs_jobs_item_type_1_workflow_as_code_status.additional_properties = d
        return extended_jobs_jobs_item_type_1_workflow_as_code_status

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
