from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.transfer_drafts_response_200_conflicts_item import TransferDraftsResponse200ConflictsItem
    from ..models.transfer_drafts_response_200_copied_item import TransferDraftsResponse200CopiedItem
    from ..models.transfer_drafts_response_200_removed_item import TransferDraftsResponse200RemovedItem


T = TypeVar("T", bound="TransferDraftsResponse200")


@_attrs_define
class TransferDraftsResponse200:
    """
    Attributes:
        copied (List['TransferDraftsResponse200CopiedItem']):
        removed (List['TransferDraftsResponse200RemovedItem']):
        conflicts (List['TransferDraftsResponse200ConflictsItem']):
    """

    copied: List["TransferDraftsResponse200CopiedItem"]
    removed: List["TransferDraftsResponse200RemovedItem"]
    conflicts: List["TransferDraftsResponse200ConflictsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        copied = []
        for copied_item_data in self.copied:
            copied_item = copied_item_data.to_dict()

            copied.append(copied_item)

        removed = []
        for removed_item_data in self.removed:
            removed_item = removed_item_data.to_dict()

            removed.append(removed_item)

        conflicts = []
        for conflicts_item_data in self.conflicts:
            conflicts_item = conflicts_item_data.to_dict()

            conflicts.append(conflicts_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "copied": copied,
                "removed": removed,
                "conflicts": conflicts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.transfer_drafts_response_200_conflicts_item import TransferDraftsResponse200ConflictsItem
        from ..models.transfer_drafts_response_200_copied_item import TransferDraftsResponse200CopiedItem
        from ..models.transfer_drafts_response_200_removed_item import TransferDraftsResponse200RemovedItem

        d = src_dict.copy()
        copied = []
        _copied = d.pop("copied")
        for copied_item_data in _copied:
            copied_item = TransferDraftsResponse200CopiedItem.from_dict(copied_item_data)

            copied.append(copied_item)

        removed = []
        _removed = d.pop("removed")
        for removed_item_data in _removed:
            removed_item = TransferDraftsResponse200RemovedItem.from_dict(removed_item_data)

            removed.append(removed_item)

        conflicts = []
        _conflicts = d.pop("conflicts")
        for conflicts_item_data in _conflicts:
            conflicts_item = TransferDraftsResponse200ConflictsItem.from_dict(conflicts_item_data)

            conflicts.append(conflicts_item)

        transfer_drafts_response_200 = cls(
            copied=copied,
            removed=removed,
            conflicts=conflicts,
        )

        transfer_drafts_response_200.additional_properties = d
        return transfer_drafts_response_200

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
