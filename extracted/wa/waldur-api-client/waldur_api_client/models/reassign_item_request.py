from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReassignItemRequest")


@_attrs_define
class ReassignItemRequest:
    """
    Attributes:
        reviewer_pool_entry_uuid (UUID): UUID of the pool entry for the new reviewer
        manager_notes (Union[Unset, str]): Notes to include in the reassignment notification
    """

    reviewer_pool_entry_uuid: UUID
    manager_notes: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reviewer_pool_entry_uuid = str(self.reviewer_pool_entry_uuid)

        manager_notes = self.manager_notes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reviewer_pool_entry_uuid": reviewer_pool_entry_uuid,
            }
        )
        if manager_notes is not UNSET:
            field_dict["manager_notes"] = manager_notes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reviewer_pool_entry_uuid = UUID(d.pop("reviewer_pool_entry_uuid"))

        manager_notes = d.pop("manager_notes", UNSET)

        reassign_item_request = cls(
            reviewer_pool_entry_uuid=reviewer_pool_entry_uuid,
            manager_notes=manager_notes,
        )

        reassign_item_request.additional_properties = d
        return reassign_item_request

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
