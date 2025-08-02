import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchJobsIndexResponse200IndexMetadata")


@_attrs_define
class SearchJobsIndexResponse200IndexMetadata:
    """Metadata about the index current state

    Attributes:
        indexed_until (Union[Unset, datetime.datetime]): Datetime of the most recently indexed job
        lost_lock_ownership (Union[Unset, bool]): Is the current indexer service being replaced
    """

    indexed_until: Union[Unset, datetime.datetime] = UNSET
    lost_lock_ownership: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        indexed_until: Union[Unset, str] = UNSET
        if not isinstance(self.indexed_until, Unset):
            indexed_until = self.indexed_until.isoformat()

        lost_lock_ownership = self.lost_lock_ownership

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if indexed_until is not UNSET:
            field_dict["indexed_until"] = indexed_until
        if lost_lock_ownership is not UNSET:
            field_dict["lost_lock_ownership"] = lost_lock_ownership

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _indexed_until = d.pop("indexed_until", UNSET)
        indexed_until: Union[Unset, datetime.datetime]
        if isinstance(_indexed_until, Unset):
            indexed_until = UNSET
        else:
            indexed_until = isoparse(_indexed_until)

        lost_lock_ownership = d.pop("lost_lock_ownership", UNSET)

        search_jobs_index_response_200_index_metadata = cls(
            indexed_until=indexed_until,
            lost_lock_ownership=lost_lock_ownership,
        )

        search_jobs_index_response_200_index_metadata.additional_properties = d
        return search_jobs_index_response_200_index_metadata

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
