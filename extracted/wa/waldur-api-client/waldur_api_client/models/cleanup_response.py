from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cleanup_response_items_item import CleanupResponseItemsItem


T = TypeVar("T", bound="CleanupResponse")


@_attrs_define
class CleanupResponse:
    """
    Attributes:
        deleted_count (int): Number of items deleted (or would be deleted in dry run)
        dry_run (bool): Whether this was a dry run
        items (list['CleanupResponseItemsItem']): List of deleted (or to-be-deleted) items
    """

    deleted_count: int
    dry_run: bool
    items: list["CleanupResponseItemsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deleted_count = self.deleted_count

        dry_run = self.dry_run

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deleted_count": deleted_count,
                "dry_run": dry_run,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cleanup_response_items_item import CleanupResponseItemsItem

        d = dict(src_dict)
        deleted_count = d.pop("deleted_count")

        dry_run = d.pop("dry_run")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = CleanupResponseItemsItem.from_dict(items_item_data)

            items.append(items_item)

        cleanup_response = cls(
            deleted_count=deleted_count,
            dry_run=dry_run,
            items=items,
        )

        cleanup_response.additional_properties = d
        return cleanup_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
