import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetResourceHistoryResponse200VersionsItem")


@_attrs_define
class GetResourceHistoryResponse200VersionsItem:
    """
    Attributes:
        id (int): How this version is addressed. Unique across every resource, so it says nothing about how many times
            this one has been saved.
        version (int): Which version of this resource it is, counted from its first. What a version is called.
        created_at (datetime.datetime):
        created_by (Union[Unset, str]):
    """

    id: int
    version: int
    created_at: datetime.datetime
    created_by: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        version = self.version
        created_at = self.created_at.isoformat()

        created_by = self.created_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "version": version,
                "created_at": created_at,
            }
        )
        if created_by is not UNSET:
            field_dict["created_by"] = created_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        version = d.pop("version")

        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by", UNSET)

        get_resource_history_response_200_versions_item = cls(
            id=id,
            version=version,
            created_at=created_at,
            created_by=created_by,
        )

        get_resource_history_response_200_versions_item.additional_properties = d
        return get_resource_history_response_200_versions_item

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
