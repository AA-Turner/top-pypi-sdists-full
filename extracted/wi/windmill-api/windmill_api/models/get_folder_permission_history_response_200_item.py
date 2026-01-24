import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetFolderPermissionHistoryResponse200Item")


@_attrs_define
class GetFolderPermissionHistoryResponse200Item:
    """
    Attributes:
        id (Union[Unset, int]):
        changed_by (Union[Unset, str]):
        changed_at (Union[Unset, datetime.datetime]):
        change_type (Union[Unset, str]):
        affected (Union[Unset, None, str]):
    """

    id: Union[Unset, int] = UNSET
    changed_by: Union[Unset, str] = UNSET
    changed_at: Union[Unset, datetime.datetime] = UNSET
    change_type: Union[Unset, str] = UNSET
    affected: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        changed_by = self.changed_by
        changed_at: Union[Unset, str] = UNSET
        if not isinstance(self.changed_at, Unset):
            changed_at = self.changed_at.isoformat()

        change_type = self.change_type
        affected = self.affected

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if changed_by is not UNSET:
            field_dict["changed_by"] = changed_by
        if changed_at is not UNSET:
            field_dict["changed_at"] = changed_at
        if change_type is not UNSET:
            field_dict["change_type"] = change_type
        if affected is not UNSET:
            field_dict["affected"] = affected

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        changed_by = d.pop("changed_by", UNSET)

        _changed_at = d.pop("changed_at", UNSET)
        changed_at: Union[Unset, datetime.datetime]
        if isinstance(_changed_at, Unset):
            changed_at = UNSET
        else:
            changed_at = isoparse(_changed_at)

        change_type = d.pop("change_type", UNSET)

        affected = d.pop("affected", UNSET)

        get_folder_permission_history_response_200_item = cls(
            id=id,
            changed_by=changed_by,
            changed_at=changed_at,
            change_type=change_type,
            affected=affected,
        )

        get_folder_permission_history_response_200_item.additional_properties = d
        return get_folder_permission_history_response_200_item

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
