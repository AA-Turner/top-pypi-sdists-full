from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetIndexDiskStorageSizesResponse200")


@_attrs_define
class GetIndexDiskStorageSizesResponse200:
    """
    Attributes:
        job_index_disk_size_bytes (Union[Unset, None, int]):
        log_index_disk_size_bytes (Union[Unset, None, int]):
    """

    job_index_disk_size_bytes: Union[Unset, None, int] = UNSET
    log_index_disk_size_bytes: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_index_disk_size_bytes = self.job_index_disk_size_bytes
        log_index_disk_size_bytes = self.log_index_disk_size_bytes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_index_disk_size_bytes is not UNSET:
            field_dict["job_index_disk_size_bytes"] = job_index_disk_size_bytes
        if log_index_disk_size_bytes is not UNSET:
            field_dict["log_index_disk_size_bytes"] = log_index_disk_size_bytes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_index_disk_size_bytes = d.pop("job_index_disk_size_bytes", UNSET)

        log_index_disk_size_bytes = d.pop("log_index_disk_size_bytes", UNSET)

        get_index_disk_storage_sizes_response_200 = cls(
            job_index_disk_size_bytes=job_index_disk_size_bytes,
            log_index_disk_size_bytes=log_index_disk_size_bytes,
        )

        get_index_disk_storage_sizes_response_200.additional_properties = d
        return get_index_disk_storage_sizes_response_200

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
