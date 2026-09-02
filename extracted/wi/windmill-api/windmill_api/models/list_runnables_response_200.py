from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_runnables_response_200_items_item import ListRunnablesResponse200ItemsItem


T = TypeVar("T", bound="ListRunnablesResponse200")


@_attrs_define
class ListRunnablesResponse200:
    """
    Attributes:
        items (List['ListRunnablesResponse200ItemsItem']):
        next_cursor (Union[Unset, str]):
    """

    items: List["ListRunnablesResponse200ItemsItem"]
    next_cursor: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()

            items.append(items_item)

        next_cursor = self.next_cursor

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
            }
        )
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_runnables_response_200_items_item import ListRunnablesResponse200ItemsItem

        d = src_dict.copy()
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = ListRunnablesResponse200ItemsItem.from_dict(items_item_data)

            items.append(items_item)

        next_cursor = d.pop("next_cursor", UNSET)

        list_runnables_response_200 = cls(
            items=items,
            next_cursor=next_cursor,
        )

        list_runnables_response_200.additional_properties = d
        return list_runnables_response_200

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
