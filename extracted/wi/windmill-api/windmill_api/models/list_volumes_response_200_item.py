import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_volumes_response_200_item_extra_perms import ListVolumesResponse200ItemExtraPerms


T = TypeVar("T", bound="ListVolumesResponse200Item")


@_attrs_define
class ListVolumesResponse200Item:
    """
    Attributes:
        name (str):
        size_bytes (int):
        file_count (int):
        created_at (datetime.datetime):
        created_by (str):
        updated_at (Union[Unset, None, datetime.datetime]):
        last_used_at (Union[Unset, None, datetime.datetime]):
        extra_perms (Union[Unset, ListVolumesResponse200ItemExtraPerms]):
    """

    name: str
    size_bytes: int
    file_count: int
    created_at: datetime.datetime
    created_by: str
    updated_at: Union[Unset, None, datetime.datetime] = UNSET
    last_used_at: Union[Unset, None, datetime.datetime] = UNSET
    extra_perms: Union[Unset, "ListVolumesResponse200ItemExtraPerms"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        size_bytes = self.size_bytes
        file_count = self.file_count
        created_at = self.created_at.isoformat()

        created_by = self.created_by
        updated_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat() if self.updated_at else None

        last_used_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_used_at, Unset):
            last_used_at = self.last_used_at.isoformat() if self.last_used_at else None

        extra_perms: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extra_perms, Unset):
            extra_perms = self.extra_perms.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "size_bytes": size_bytes,
                "file_count": file_count,
                "created_at": created_at,
                "created_by": created_by,
            }
        )
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at
        if extra_perms is not UNSET:
            field_dict["extra_perms"] = extra_perms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_volumes_response_200_item_extra_perms import ListVolumesResponse200ItemExtraPerms

        d = src_dict.copy()
        name = d.pop("name")

        size_bytes = d.pop("size_bytes")

        file_count = d.pop("file_count")

        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, None, datetime.datetime]
        if _updated_at is None:
            updated_at = None
        elif isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        _last_used_at = d.pop("last_used_at", UNSET)
        last_used_at: Union[Unset, None, datetime.datetime]
        if _last_used_at is None:
            last_used_at = None
        elif isinstance(_last_used_at, Unset):
            last_used_at = UNSET
        else:
            last_used_at = isoparse(_last_used_at)

        _extra_perms = d.pop("extra_perms", UNSET)
        extra_perms: Union[Unset, ListVolumesResponse200ItemExtraPerms]
        if isinstance(_extra_perms, Unset):
            extra_perms = UNSET
        else:
            extra_perms = ListVolumesResponse200ItemExtraPerms.from_dict(_extra_perms)

        list_volumes_response_200_item = cls(
            name=name,
            size_bytes=size_bytes,
            file_count=file_count,
            created_at=created_at,
            created_by=created_by,
            updated_at=updated_at,
            last_used_at=last_used_at,
            extra_perms=extra_perms,
        )

        list_volumes_response_200_item.additional_properties = d
        return list_volumes_response_200_item

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
