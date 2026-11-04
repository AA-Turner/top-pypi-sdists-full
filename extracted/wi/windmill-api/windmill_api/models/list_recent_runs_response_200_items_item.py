from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

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
        status (ListRecentRunsResponse200ItemsItemStatus): a failure someone or something marked as handled is
            `resolved`, not `failure`
        failed_runs (int): unresolved failed runs of the item over the whole window, not only those in runs
        runs (List['ListRecentRunsResponse200ItemsItemRunsItem']):
        summary (Union[Unset, str]):
        failed_run_ids (Union[Unset, List[str]]): the ids of those failed runs, only for the item named by
            failed_ids_kind and failed_ids_path
    """

    path: str
    kind: ListRecentRunsResponse200ItemsItemKind
    status: ListRecentRunsResponse200ItemsItemStatus
    failed_runs: int
    runs: List["ListRecentRunsResponse200ItemsItemRunsItem"]
    summary: Union[Unset, str] = UNSET
    failed_run_ids: Union[Unset, List[str]] = UNSET
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
        failed_run_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.failed_run_ids, Unset):
            failed_run_ids = self.failed_run_ids

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
        if failed_run_ids is not UNSET:
            field_dict["failed_run_ids"] = failed_run_ids

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

        failed_run_ids = cast(List[str], d.pop("failed_run_ids", UNSET))

        list_recent_runs_response_200_items_item = cls(
            path=path,
            kind=kind,
            status=status,
            failed_runs=failed_runs,
            runs=runs,
            summary=summary,
            failed_run_ids=failed_run_ids,
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
