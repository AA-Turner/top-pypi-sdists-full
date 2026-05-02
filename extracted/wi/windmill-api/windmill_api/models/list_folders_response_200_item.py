import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_folders_response_200_item_default_permissioned_as_item import (
        ListFoldersResponse200ItemDefaultPermissionedAsItem,
    )
    from ..models.list_folders_response_200_item_extra_perms import ListFoldersResponse200ItemExtraPerms


T = TypeVar("T", bound="ListFoldersResponse200Item")


@_attrs_define
class ListFoldersResponse200Item:
    """
    Attributes:
        name (str):
        owners (List[str]):
        extra_perms (ListFoldersResponse200ItemExtraPerms):
        summary (Union[Unset, str]):
        created_by (Union[Unset, str]):
        edited_at (Union[Unset, datetime.datetime]):
        default_permissioned_as (Union[Unset, List['ListFoldersResponse200ItemDefaultPermissionedAsItem']]): Ordered
            list of rules applied at create-time when admins or `wm_deployers` members deploy items in this folder. The
            first rule whose `path_glob` matches the item path (relative to the folder root) wins, and its `permissioned_as`
            is used as the default.
    """

    name: str
    owners: List[str]
    extra_perms: "ListFoldersResponse200ItemExtraPerms"
    summary: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    edited_at: Union[Unset, datetime.datetime] = UNSET
    default_permissioned_as: Union[Unset, List["ListFoldersResponse200ItemDefaultPermissionedAsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        owners = self.owners

        extra_perms = self.extra_perms.to_dict()

        summary = self.summary
        created_by = self.created_by
        edited_at: Union[Unset, str] = UNSET
        if not isinstance(self.edited_at, Unset):
            edited_at = self.edited_at.isoformat()

        default_permissioned_as: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.default_permissioned_as, Unset):
            default_permissioned_as = []
            for default_permissioned_as_item_data in self.default_permissioned_as:
                default_permissioned_as_item = default_permissioned_as_item_data.to_dict()

                default_permissioned_as.append(default_permissioned_as_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "owners": owners,
                "extra_perms": extra_perms,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if edited_at is not UNSET:
            field_dict["edited_at"] = edited_at
        if default_permissioned_as is not UNSET:
            field_dict["default_permissioned_as"] = default_permissioned_as

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_folders_response_200_item_default_permissioned_as_item import (
            ListFoldersResponse200ItemDefaultPermissionedAsItem,
        )
        from ..models.list_folders_response_200_item_extra_perms import ListFoldersResponse200ItemExtraPerms

        d = src_dict.copy()
        name = d.pop("name")

        owners = cast(List[str], d.pop("owners"))

        extra_perms = ListFoldersResponse200ItemExtraPerms.from_dict(d.pop("extra_perms"))

        summary = d.pop("summary", UNSET)

        created_by = d.pop("created_by", UNSET)

        _edited_at = d.pop("edited_at", UNSET)
        edited_at: Union[Unset, datetime.datetime]
        if isinstance(_edited_at, Unset):
            edited_at = UNSET
        else:
            edited_at = isoparse(_edited_at)

        default_permissioned_as = []
        _default_permissioned_as = d.pop("default_permissioned_as", UNSET)
        for default_permissioned_as_item_data in _default_permissioned_as or []:
            default_permissioned_as_item = ListFoldersResponse200ItemDefaultPermissionedAsItem.from_dict(
                default_permissioned_as_item_data
            )

            default_permissioned_as.append(default_permissioned_as_item)

        list_folders_response_200_item = cls(
            name=name,
            owners=owners,
            extra_perms=extra_perms,
            summary=summary,
            created_by=created_by,
            edited_at=edited_at,
            default_permissioned_as=default_permissioned_as,
        )

        list_folders_response_200_item.additional_properties = d
        return list_folders_response_200_item

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
