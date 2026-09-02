from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace_comparison_hidden_ahead_by_kind import WorkspaceComparisonHiddenAheadByKind
    from ..models.workspace_comparison_hidden_ahead_items_item import WorkspaceComparisonHiddenAheadItemsItem


T = TypeVar("T", bound="WorkspaceComparisonHiddenAhead")


@_attrs_define
class WorkspaceComparisonHiddenAhead:
    """Ahead items excluded from `diffs` because they are not visible to the caller

    Attributes:
        total (int): Total number of hidden items on this side
        by_kind (WorkspaceComparisonHiddenAheadByKind): Count of hidden items keyed by item kind (always populated)
        items (List['WorkspaceComparisonHiddenAheadItemsItem']): Kind and path of each hidden item; only populated when
            the caller is an admin of the relevant side (empty otherwise)
    """

    total: int
    by_kind: "WorkspaceComparisonHiddenAheadByKind"
    items: List["WorkspaceComparisonHiddenAheadItemsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total = self.total
        by_kind = self.by_kind.to_dict()

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()

            items.append(items_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "by_kind": by_kind,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workspace_comparison_hidden_ahead_by_kind import WorkspaceComparisonHiddenAheadByKind
        from ..models.workspace_comparison_hidden_ahead_items_item import WorkspaceComparisonHiddenAheadItemsItem

        d = src_dict.copy()
        total = d.pop("total")

        by_kind = WorkspaceComparisonHiddenAheadByKind.from_dict(d.pop("by_kind"))

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = WorkspaceComparisonHiddenAheadItemsItem.from_dict(items_item_data)

            items.append(items_item)

        workspace_comparison_hidden_ahead = cls(
            total=total,
            by_kind=by_kind,
            items=items,
        )

        workspace_comparison_hidden_ahead.additional_properties = d
        return workspace_comparison_hidden_ahead

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
