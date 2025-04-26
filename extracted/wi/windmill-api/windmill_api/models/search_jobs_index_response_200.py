from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_jobs_index_response_200_hits_item import SearchJobsIndexResponse200HitsItem
    from ..models.search_jobs_index_response_200_query_parse_errors_item import (
        SearchJobsIndexResponse200QueryParseErrorsItem,
    )


T = TypeVar("T", bound="SearchJobsIndexResponse200")


@_attrs_define
class SearchJobsIndexResponse200:
    """
    Attributes:
        query_parse_errors (Union[Unset, List['SearchJobsIndexResponse200QueryParseErrorsItem']]): a list of the terms
            that couldn't be parsed (and thus ignored)
        hits (Union[Unset, List['SearchJobsIndexResponse200HitsItem']]): the jobs that matched the query
    """

    query_parse_errors: Union[Unset, List["SearchJobsIndexResponse200QueryParseErrorsItem"]] = UNSET
    hits: Union[Unset, List["SearchJobsIndexResponse200HitsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query_parse_errors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.query_parse_errors, Unset):
            query_parse_errors = []
            for query_parse_errors_item_data in self.query_parse_errors:
                query_parse_errors_item = query_parse_errors_item_data.to_dict()

                query_parse_errors.append(query_parse_errors_item)

        hits: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.hits, Unset):
            hits = []
            for hits_item_data in self.hits:
                hits_item = hits_item_data.to_dict()

                hits.append(hits_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if query_parse_errors is not UNSET:
            field_dict["query_parse_errors"] = query_parse_errors
        if hits is not UNSET:
            field_dict["hits"] = hits

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.search_jobs_index_response_200_hits_item import SearchJobsIndexResponse200HitsItem
        from ..models.search_jobs_index_response_200_query_parse_errors_item import (
            SearchJobsIndexResponse200QueryParseErrorsItem,
        )

        d = src_dict.copy()
        query_parse_errors = []
        _query_parse_errors = d.pop("query_parse_errors", UNSET)
        for query_parse_errors_item_data in _query_parse_errors or []:
            query_parse_errors_item = SearchJobsIndexResponse200QueryParseErrorsItem.from_dict(
                query_parse_errors_item_data
            )

            query_parse_errors.append(query_parse_errors_item)

        hits = []
        _hits = d.pop("hits", UNSET)
        for hits_item_data in _hits or []:
            hits_item = SearchJobsIndexResponse200HitsItem.from_dict(hits_item_data)

            hits.append(hits_item)

        search_jobs_index_response_200 = cls(
            query_parse_errors=query_parse_errors,
            hits=hits,
        )

        search_jobs_index_response_200.additional_properties = d
        return search_jobs_index_response_200

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
