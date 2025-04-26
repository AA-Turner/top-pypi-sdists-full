import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAutoscalingEventsResponse200Item")


@_attrs_define
class ListAutoscalingEventsResponse200Item:
    """
    Attributes:
        id (Union[Unset, int]):
        worker_group (Union[Unset, str]):
        event_type (Union[Unset, str]):
        desired_workers (Union[Unset, int]):
        reason (Union[Unset, str]):
        applied_at (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, int] = UNSET
    worker_group: Union[Unset, str] = UNSET
    event_type: Union[Unset, str] = UNSET
    desired_workers: Union[Unset, int] = UNSET
    reason: Union[Unset, str] = UNSET
    applied_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        worker_group = self.worker_group
        event_type = self.event_type
        desired_workers = self.desired_workers
        reason = self.reason
        applied_at: Union[Unset, str] = UNSET
        if not isinstance(self.applied_at, Unset):
            applied_at = self.applied_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if worker_group is not UNSET:
            field_dict["worker_group"] = worker_group
        if event_type is not UNSET:
            field_dict["event_type"] = event_type
        if desired_workers is not UNSET:
            field_dict["desired_workers"] = desired_workers
        if reason is not UNSET:
            field_dict["reason"] = reason
        if applied_at is not UNSET:
            field_dict["applied_at"] = applied_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        worker_group = d.pop("worker_group", UNSET)

        event_type = d.pop("event_type", UNSET)

        desired_workers = d.pop("desired_workers", UNSET)

        reason = d.pop("reason", UNSET)

        _applied_at = d.pop("applied_at", UNSET)
        applied_at: Union[Unset, datetime.datetime]
        if isinstance(_applied_at, Unset):
            applied_at = UNSET
        else:
            applied_at = isoparse(_applied_at)

        list_autoscaling_events_response_200_item = cls(
            id=id,
            worker_group=worker_group,
            event_type=event_type,
            desired_workers=desired_workers,
            reason=reason,
            applied_at=applied_at,
        )

        list_autoscaling_events_response_200_item.additional_properties = d
        return list_autoscaling_events_response_200_item

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
