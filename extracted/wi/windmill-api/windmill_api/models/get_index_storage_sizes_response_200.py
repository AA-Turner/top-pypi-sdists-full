from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_index_storage_sizes_response_200_job_index import GetIndexStorageSizesResponse200JobIndex
    from ..models.get_index_storage_sizes_response_200_service_log_index import (
        GetIndexStorageSizesResponse200ServiceLogIndex,
    )


T = TypeVar("T", bound="GetIndexStorageSizesResponse200")


@_attrs_define
class GetIndexStorageSizesResponse200:
    """
    Attributes:
        job_index (Union[Unset, GetIndexStorageSizesResponse200JobIndex]):
        service_log_index (Union[Unset, GetIndexStorageSizesResponse200ServiceLogIndex]):
    """

    job_index: Union[Unset, "GetIndexStorageSizesResponse200JobIndex"] = UNSET
    service_log_index: Union[Unset, "GetIndexStorageSizesResponse200ServiceLogIndex"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_index: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.job_index, Unset):
            job_index = self.job_index.to_dict()

        service_log_index: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.service_log_index, Unset):
            service_log_index = self.service_log_index.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_index is not UNSET:
            field_dict["job_index"] = job_index
        if service_log_index is not UNSET:
            field_dict["service_log_index"] = service_log_index

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_index_storage_sizes_response_200_job_index import GetIndexStorageSizesResponse200JobIndex
        from ..models.get_index_storage_sizes_response_200_service_log_index import (
            GetIndexStorageSizesResponse200ServiceLogIndex,
        )

        d = src_dict.copy()
        _job_index = d.pop("job_index", UNSET)
        job_index: Union[Unset, GetIndexStorageSizesResponse200JobIndex]
        if isinstance(_job_index, Unset):
            job_index = UNSET
        else:
            job_index = GetIndexStorageSizesResponse200JobIndex.from_dict(_job_index)

        _service_log_index = d.pop("service_log_index", UNSET)
        service_log_index: Union[Unset, GetIndexStorageSizesResponse200ServiceLogIndex]
        if isinstance(_service_log_index, Unset):
            service_log_index = UNSET
        else:
            service_log_index = GetIndexStorageSizesResponse200ServiceLogIndex.from_dict(_service_log_index)

        get_index_storage_sizes_response_200 = cls(
            job_index=job_index,
            service_log_index=service_log_index,
        )

        get_index_storage_sizes_response_200.additional_properties = d
        return get_index_storage_sizes_response_200

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
