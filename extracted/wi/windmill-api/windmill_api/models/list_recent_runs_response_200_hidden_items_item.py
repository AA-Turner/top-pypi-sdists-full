from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_recent_runs_response_200_hidden_items_item_kind import ListRecentRunsResponse200HiddenItemsItemKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListRecentRunsResponse200HiddenItemsItem")


@_attrs_define
class ListRecentRunsResponse200HiddenItemsItem:
    """
    Attributes:
        kind (ListRecentRunsResponse200HiddenItemsItemKind):
        path (str):
        summary (Union[Unset, str]):
    """

    kind: ListRecentRunsResponse200HiddenItemsItemKind
    path: str
    summary: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        path = self.path
        summary = self.summary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "path": path,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kind = ListRecentRunsResponse200HiddenItemsItemKind(d.pop("kind"))

        path = d.pop("path")

        summary = d.pop("summary", UNSET)

        list_recent_runs_response_200_hidden_items_item = cls(
            kind=kind,
            path=path,
            summary=summary,
        )

        list_recent_runs_response_200_hidden_items_item.additional_properties = d
        return list_recent_runs_response_200_hidden_items_item

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
