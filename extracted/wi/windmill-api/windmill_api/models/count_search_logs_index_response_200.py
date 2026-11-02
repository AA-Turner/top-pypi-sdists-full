from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.count_search_logs_index_response_200_count_per_host import CountSearchLogsIndexResponse200CountPerHost


T = TypeVar("T", bound="CountSearchLogsIndexResponse200")


@_attrs_define
class CountSearchLogsIndexResponse200:
    """
    Attributes:
        query_parse_errors (Union[Unset, List[str]]): a list of the terms that couldn't be parsed (and thus ignored)
        count_per_host (Union[Unset, CountSearchLogsIndexResponse200CountPerHost]): count of log lines that matched the
            query per hostname
    """

    query_parse_errors: Union[Unset, List[str]] = UNSET
    count_per_host: Union[Unset, "CountSearchLogsIndexResponse200CountPerHost"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query_parse_errors: Union[Unset, List[str]] = UNSET
        if not isinstance(self.query_parse_errors, Unset):
            query_parse_errors = self.query_parse_errors

        count_per_host: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.count_per_host, Unset):
            count_per_host = self.count_per_host.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if query_parse_errors is not UNSET:
            field_dict["query_parse_errors"] = query_parse_errors
        if count_per_host is not UNSET:
            field_dict["count_per_host"] = count_per_host

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.count_search_logs_index_response_200_count_per_host import (
            CountSearchLogsIndexResponse200CountPerHost,
        )

        d = src_dict.copy()
        query_parse_errors = cast(List[str], d.pop("query_parse_errors", UNSET))

        _count_per_host = d.pop("count_per_host", UNSET)
        count_per_host: Union[Unset, CountSearchLogsIndexResponse200CountPerHost]
        if isinstance(_count_per_host, Unset):
            count_per_host = UNSET
        else:
            count_per_host = CountSearchLogsIndexResponse200CountPerHost.from_dict(_count_per_host)

        count_search_logs_index_response_200 = cls(
            query_parse_errors=query_parse_errors,
            count_per_host=count_per_host,
        )

        count_search_logs_index_response_200.additional_properties = d
        return count_search_logs_index_response_200

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
