from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transfer_drafts_json_body_items_item import TransferDraftsJsonBodyItemsItem


T = TypeVar("T", bound="TransferDraftsJsonBody")


@_attrs_define
class TransferDraftsJsonBody:
    """
    Attributes:
        items (List['TransferDraftsJsonBodyItemsItem']):
        target_workspace (Union[Unset, str]):
        remove_from_source (Union[Unset, bool]):
        replace_existing (Union[Unset, bool]): Overwrite the user's own drafts of `items` already in the target instead
            of returning them as conflicts.
    """

    items: List["TransferDraftsJsonBodyItemsItem"]
    target_workspace: Union[Unset, str] = UNSET
    remove_from_source: Union[Unset, bool] = UNSET
    replace_existing: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()

            items.append(items_item)

        target_workspace = self.target_workspace
        remove_from_source = self.remove_from_source
        replace_existing = self.replace_existing

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
            }
        )
        if target_workspace is not UNSET:
            field_dict["target_workspace"] = target_workspace
        if remove_from_source is not UNSET:
            field_dict["remove_from_source"] = remove_from_source
        if replace_existing is not UNSET:
            field_dict["replace_existing"] = replace_existing

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.transfer_drafts_json_body_items_item import TransferDraftsJsonBodyItemsItem

        d = src_dict.copy()
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = TransferDraftsJsonBodyItemsItem.from_dict(items_item_data)

            items.append(items_item)

        target_workspace = d.pop("target_workspace", UNSET)

        remove_from_source = d.pop("remove_from_source", UNSET)

        replace_existing = d.pop("replace_existing", UNSET)

        transfer_drafts_json_body = cls(
            items=items,
            target_workspace=target_workspace,
            remove_from_source=remove_from_source,
            replace_existing=replace_existing,
        )

        transfer_drafts_json_body.additional_properties = d
        return transfer_drafts_json_body

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
