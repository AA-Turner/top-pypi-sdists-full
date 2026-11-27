from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offboard_response_conflict_items_item import OffboardResponseConflictItemsItem
    from ..models.offboard_response_summary import OffboardResponseSummary


T = TypeVar("T", bound="OffboardResponse")


@_attrs_define
class OffboardResponse:
    """
    Attributes:
        conflicts (Union[Unset, List[str]]): List of path conflicts that block the offboarding. Empty on success.
        conflict_items (Union[Unset, List['OffboardResponseConflictItemsItem']]): The same conflicts as `conflicts`,
            structured. Empty on success.
        summary (Union[Unset, OffboardResponseSummary]):
    """

    conflicts: Union[Unset, List[str]] = UNSET
    conflict_items: Union[Unset, List["OffboardResponseConflictItemsItem"]] = UNSET
    summary: Union[Unset, "OffboardResponseSummary"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        conflicts: Union[Unset, List[str]] = UNSET
        if not isinstance(self.conflicts, Unset):
            conflicts = self.conflicts

        conflict_items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.conflict_items, Unset):
            conflict_items = []
            for conflict_items_item_data in self.conflict_items:
                conflict_items_item = conflict_items_item_data.to_dict()

                conflict_items.append(conflict_items_item)

        summary: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.summary, Unset):
            summary = self.summary.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if conflicts is not UNSET:
            field_dict["conflicts"] = conflicts
        if conflict_items is not UNSET:
            field_dict["conflict_items"] = conflict_items
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.offboard_response_conflict_items_item import OffboardResponseConflictItemsItem
        from ..models.offboard_response_summary import OffboardResponseSummary

        d = src_dict.copy()
        conflicts = cast(List[str], d.pop("conflicts", UNSET))

        conflict_items = []
        _conflict_items = d.pop("conflict_items", UNSET)
        for conflict_items_item_data in _conflict_items or []:
            conflict_items_item = OffboardResponseConflictItemsItem.from_dict(conflict_items_item_data)

            conflict_items.append(conflict_items_item)

        _summary = d.pop("summary", UNSET)
        summary: Union[Unset, OffboardResponseSummary]
        if isinstance(_summary, Unset):
            summary = UNSET
        else:
            summary = OffboardResponseSummary.from_dict(_summary)

        offboard_response = cls(
            conflicts=conflicts,
            conflict_items=conflict_items,
            summary=summary,
        )

        offboard_response.additional_properties = d
        return offboard_response

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
