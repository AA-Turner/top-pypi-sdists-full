import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="GetStorageUsageResponse200StoragesItem")


@_attrs_define
class GetStorageUsageResponse200StoragesItem:
    """
    Attributes:
        storage (str):
        bytes_ (int):
        computed_at (datetime.datetime):
    """

    storage: str
    bytes_: int
    computed_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        storage = self.storage
        bytes_ = self.bytes_
        computed_at = self.computed_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "storage": storage,
                "bytes": bytes_,
                "computed_at": computed_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        storage = d.pop("storage")

        bytes_ = d.pop("bytes")

        computed_at = isoparse(d.pop("computed_at"))

        get_storage_usage_response_200_storages_item = cls(
            storage=storage,
            bytes_=bytes_,
            computed_at=computed_at,
        )

        get_storage_usage_response_200_storages_item.additional_properties = d
        return get_storage_usage_response_200_storages_item

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
