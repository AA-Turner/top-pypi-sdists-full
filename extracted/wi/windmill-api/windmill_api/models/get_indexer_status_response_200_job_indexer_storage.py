from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetIndexerStatusResponse200JobIndexerStorage")


@_attrs_define
class GetIndexerStatusResponse200JobIndexerStorage:
    """
    Attributes:
        disk_size_bytes (Union[Unset, None, int]):
        s3_size_bytes (Union[Unset, None, int]):
    """

    disk_size_bytes: Union[Unset, None, int] = UNSET
    s3_size_bytes: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        disk_size_bytes = self.disk_size_bytes
        s3_size_bytes = self.s3_size_bytes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if disk_size_bytes is not UNSET:
            field_dict["disk_size_bytes"] = disk_size_bytes
        if s3_size_bytes is not UNSET:
            field_dict["s3_size_bytes"] = s3_size_bytes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        disk_size_bytes = d.pop("disk_size_bytes", UNSET)

        s3_size_bytes = d.pop("s3_size_bytes", UNSET)

        get_indexer_status_response_200_job_indexer_storage = cls(
            disk_size_bytes=disk_size_bytes,
            s3_size_bytes=s3_size_bytes,
        )

        get_indexer_status_response_200_job_indexer_storage.additional_properties = d
        return get_indexer_status_response_200_job_indexer_storage

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
