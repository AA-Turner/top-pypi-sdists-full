from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_recent_runs_response_200_items_item import ListRecentRunsResponse200ItemsItem


T = TypeVar("T", bound="ListRecentRunsResponse200")


@_attrs_define
class ListRecentRunsResponse200:
    """
    Attributes:
        window_hours (int):
        capped (bool): the window holds more runs than were read, so counts cover the newest ones only
        total_runs (int):
        failed_runs (int):
        failing_items (int):
        running_items (int):
        items (List['ListRecentRunsResponse200ItemsItem']):
    """

    window_hours: int
    capped: bool
    total_runs: int
    failed_runs: int
    failing_items: int
    running_items: int
    items: List["ListRecentRunsResponse200ItemsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        window_hours = self.window_hours
        capped = self.capped
        total_runs = self.total_runs
        failed_runs = self.failed_runs
        failing_items = self.failing_items
        running_items = self.running_items
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()

            items.append(items_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "window_hours": window_hours,
                "capped": capped,
                "total_runs": total_runs,
                "failed_runs": failed_runs,
                "failing_items": failing_items,
                "running_items": running_items,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_recent_runs_response_200_items_item import ListRecentRunsResponse200ItemsItem

        d = src_dict.copy()
        window_hours = d.pop("window_hours")

        capped = d.pop("capped")

        total_runs = d.pop("total_runs")

        failed_runs = d.pop("failed_runs")

        failing_items = d.pop("failing_items")

        running_items = d.pop("running_items")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = ListRecentRunsResponse200ItemsItem.from_dict(items_item_data)

            items.append(items_item)

        list_recent_runs_response_200 = cls(
            window_hours=window_hours,
            capped=capped,
            total_runs=total_runs,
            failed_runs=failed_runs,
            failing_items=failing_items,
            running_items=running_items,
            items=items,
        )

        list_recent_runs_response_200.additional_properties = d
        return list_recent_runs_response_200

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
