import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_recent_runs_response_200_items_item_runs_item_status import (
    ListRecentRunsResponse200ItemsItemRunsItemStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListRecentRunsResponse200ItemsItemRunsItem")


@_attrs_define
class ListRecentRunsResponse200ItemsItemRunsItem:
    """
    Attributes:
        id (str):
        status (ListRecentRunsResponse200ItemsItemRunsItemStatus):
        ran_at (datetime.datetime): when the run started, or was created for one that has not reported a start
        duration_ms (Union[Unset, int]):
    """

    id: str
    status: ListRecentRunsResponse200ItemsItemRunsItemStatus
    ran_at: datetime.datetime
    duration_ms: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        status = self.status.value

        ran_at = self.ran_at.isoformat()

        duration_ms = self.duration_ms

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "ran_at": ran_at,
            }
        )
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        status = ListRecentRunsResponse200ItemsItemRunsItemStatus(d.pop("status"))

        ran_at = isoparse(d.pop("ran_at"))

        duration_ms = d.pop("duration_ms", UNSET)

        list_recent_runs_response_200_items_item_runs_item = cls(
            id=id,
            status=status,
            ran_at=ran_at,
            duration_ms=duration_ms,
        )

        list_recent_runs_response_200_items_item_runs_item.additional_properties = d
        return list_recent_runs_response_200_items_item_runs_item

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
