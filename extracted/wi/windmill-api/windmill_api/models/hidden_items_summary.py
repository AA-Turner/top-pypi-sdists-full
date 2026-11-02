from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.hidden_items_summary_by_kind import HiddenItemsSummaryByKind
    from ..models.hidden_items_summary_items_item import HiddenItemsSummaryItemsItem


T = TypeVar("T", bound="HiddenItemsSummary")


@_attrs_define
class HiddenItemsSummary:
    """
    Attributes:
        total (int): Total number of hidden items on this side
        by_kind (HiddenItemsSummaryByKind): Count of hidden items keyed by item kind (always populated)
        items (List['HiddenItemsSummaryItemsItem']): Kind and path of each hidden item; only populated when the caller
            is an admin of the relevant side (empty otherwise)
    """

    total: int
    by_kind: "HiddenItemsSummaryByKind"
    items: List["HiddenItemsSummaryItemsItem"]
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
        from ..models.hidden_items_summary_by_kind import HiddenItemsSummaryByKind
        from ..models.hidden_items_summary_items_item import HiddenItemsSummaryItemsItem

        d = src_dict.copy()
        total = d.pop("total")

        by_kind = HiddenItemsSummaryByKind.from_dict(d.pop("by_kind"))

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = HiddenItemsSummaryItemsItem.from_dict(items_item_data)

            items.append(items_item)

        hidden_items_summary = cls(
            total=total,
            by_kind=by_kind,
            items=items,
        )

        hidden_items_summary.additional_properties = d
        return hidden_items_summary

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
