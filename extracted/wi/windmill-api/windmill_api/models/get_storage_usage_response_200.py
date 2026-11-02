from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_storage_usage_response_200_storages_item import GetStorageUsageResponse200StoragesItem


T = TypeVar("T", bound="GetStorageUsageResponse200")


@_attrs_define
class GetStorageUsageResponse200:
    """
    Attributes:
        total_bytes (int):
        storages (List['GetStorageUsageResponse200StoragesItem']):
        quota_bytes (Union[Unset, int]): only present on Community Edition, where workspace storage is capped
    """

    total_bytes: int
    storages: List["GetStorageUsageResponse200StoragesItem"]
    quota_bytes: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_bytes = self.total_bytes
        storages = []
        for storages_item_data in self.storages:
            storages_item = storages_item_data.to_dict()

            storages.append(storages_item)

        quota_bytes = self.quota_bytes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_bytes": total_bytes,
                "storages": storages,
            }
        )
        if quota_bytes is not UNSET:
            field_dict["quota_bytes"] = quota_bytes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_storage_usage_response_200_storages_item import GetStorageUsageResponse200StoragesItem

        d = src_dict.copy()
        total_bytes = d.pop("total_bytes")

        storages = []
        _storages = d.pop("storages")
        for storages_item_data in _storages:
            storages_item = GetStorageUsageResponse200StoragesItem.from_dict(storages_item_data)

            storages.append(storages_item)

        quota_bytes = d.pop("quota_bytes", UNSET)

        get_storage_usage_response_200 = cls(
            total_bytes=total_bytes,
            storages=storages,
            quota_bytes=quota_bytes,
        )

        get_storage_usage_response_200.additional_properties = d
        return get_storage_usage_response_200

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
