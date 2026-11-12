from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trigger_ci_tests_batch_json_body_items_item import TriggerCiTestsBatchJsonBodyItemsItem


T = TypeVar("T", bound="TriggerCiTestsBatchJsonBody")


@_attrs_define
class TriggerCiTestsBatchJsonBody:
    """
    Attributes:
        items (List['TriggerCiTestsBatchJsonBodyItemsItem']):
        ignore_pending (Union[Unset, bool]):
    """

    items: List["TriggerCiTestsBatchJsonBodyItemsItem"]
    ignore_pending: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()

            items.append(items_item)

        ignore_pending = self.ignore_pending

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
            }
        )
        if ignore_pending is not UNSET:
            field_dict["ignore_pending"] = ignore_pending

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.trigger_ci_tests_batch_json_body_items_item import TriggerCiTestsBatchJsonBodyItemsItem

        d = src_dict.copy()
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = TriggerCiTestsBatchJsonBodyItemsItem.from_dict(items_item_data)

            items.append(items_item)

        ignore_pending = d.pop("ignore_pending", UNSET)

        trigger_ci_tests_batch_json_body = cls(
            items=items,
            ignore_pending=ignore_pending,
        )

        trigger_ci_tests_batch_json_body.additional_properties = d
        return trigger_ci_tests_batch_json_body

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
