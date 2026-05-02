from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetObjectStorageUsageResponse200FoldersItem")


@_attrs_define
class GetObjectStorageUsageResponse200FoldersItem:
    """
    Attributes:
        prefix (str):
        size (int):
        partial (Union[Unset, bool]):
    """

    prefix: str
    size: int
    partial: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prefix = self.prefix
        size = self.size
        partial = self.partial

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prefix": prefix,
                "size": size,
            }
        )
        if partial is not UNSET:
            field_dict["partial"] = partial

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        prefix = d.pop("prefix")

        size = d.pop("size")

        partial = d.pop("partial", UNSET)

        get_object_storage_usage_response_200_folders_item = cls(
            prefix=prefix,
            size=size,
            partial=partial,
        )

        get_object_storage_usage_response_200_folders_item.additional_properties = d
        return get_object_storage_usage_response_200_folders_item

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
