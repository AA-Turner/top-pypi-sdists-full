import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_folder_response_200_extra_perms import GetFolderResponse200ExtraPerms


T = TypeVar("T", bound="GetFolderResponse200")


@_attrs_define
class GetFolderResponse200:
    """
    Attributes:
        name (str):
        owners (List[str]):
        extra_perms (GetFolderResponse200ExtraPerms):
        summary (Union[Unset, str]):
        created_by (Union[Unset, str]):
        edited_at (Union[Unset, datetime.datetime]):
    """

    name: str
    owners: List[str]
    extra_perms: "GetFolderResponse200ExtraPerms"
    summary: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    edited_at: Union[Unset, datetime.datetime] = UNSET
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_folder_response_200_extra_perms import GetFolderResponse200ExtraPerms

        d = src_dict.copy()
        name = d.pop("name")

        owners = cast(List[str], d.pop("owners"))

        extra_perms = GetFolderResponse200ExtraPerms.from_dict(d.pop("extra_perms"))

        summary = d.pop("summary", UNSET)

        created_by = d.pop("created_by", UNSET)

        _edited_at = d.pop("edited_at", UNSET)
        edited_at: Union[Unset, datetime.datetime]
        if isinstance(_edited_at, Unset):
            edited_at = UNSET
        else:
            edited_at = isoparse(_edited_at)

        get_folder_response_200 = cls(
            name=name,
            owners=owners,
            extra_perms=extra_perms,
            summary=summary,
            created_by=created_by,
            edited_at=edited_at,
        )

        get_folder_response_200.additional_properties = d
        return get_folder_response_200

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
