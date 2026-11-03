from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_recent_runs_response_200_items_item_kind import ListRecentRunsResponse200ItemsItemKind
from ..models.list_recent_runs_response_200_items_item_status import ListRecentRunsResponse200ItemsItemStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_recent_runs_response_200_items_item_runs_item import ListRecentRunsResponse200ItemsItemRunsItem


T = TypeVar("T", bound="ListRecentRunsResponse200ItemsItem")


@_attrs_define
class ListRecentRunsResponse200ItemsItem:
    """
    Attributes:
        path (str):
        kind (ListRecentRunsResponse200ItemsItemKind):
        status (ListRecentRunsResponse200ItemsItemStatus):
        failed_runs (int): failed runs of the item over the whole window, not only those in runs
        runs (List['ListRecentRunsResponse200ItemsItemRunsItem']):
        summary (Union[Unset, str]):
    """

    path: str
    kind: ListRecentRunsResponse200ItemsItemKind
    status: ListRecentRunsResponse200ItemsItemStatus
    failed_runs: int
    runs: List["ListRecentRunsResponse200ItemsItemRunsItem"]
    summary: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        kind = self.kind.value

        status = self.status.value

        failed_runs = self.failed_runs
        runs = []
        for runs_item_data in self.runs:
            runs_item = runs_item_data.to_dict()

            runs.append(runs_item)

        summary = self.summary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "kind": kind,
                "status": status,
                "failed_runs": failed_runs,
                "runs": runs,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_recent_runs_response_200_items_item_runs_item import (
            ListRecentRunsResponse200ItemsItemRunsItem,
        )

        d = src_dict.copy()
        path = d.pop("path")

        kind = ListRecentRunsResponse200ItemsItemKind(d.pop("kind"))

        status = ListRecentRunsResponse200ItemsItemStatus(d.pop("status"))

        failed_runs = d.pop("failed_runs")

        runs = []
        _runs = d.pop("runs")
        for runs_item_data in _runs:
            runs_item = ListRecentRunsResponse200ItemsItemRunsItem.from_dict(runs_item_data)

            runs.append(runs_item)

        summary = d.pop("summary", UNSET)

        list_recent_runs_response_200_items_item = cls(
            path=path,
            kind=kind,
            status=status,
            failed_runs=failed_runs,
            runs=runs,
            summary=summary,
        )

        list_recent_runs_response_200_items_item.additional_properties = d
        return list_recent_runs_response_200_items_item

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
