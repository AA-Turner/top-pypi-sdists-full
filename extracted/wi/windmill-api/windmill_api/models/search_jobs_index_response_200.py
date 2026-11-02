from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_jobs_index_response_200_hits_item import SearchJobsIndexResponse200HitsItem
    from ..models.search_jobs_index_response_200_index_metadata import SearchJobsIndexResponse200IndexMetadata


T = TypeVar("T", bound="SearchJobsIndexResponse200")


@_attrs_define
class SearchJobsIndexResponse200:
    """
    Attributes:
        query_parse_errors (Union[Unset, List[str]]): a list of the terms that couldn't be parsed (and thus ignored)
        hits (Union[Unset, List['SearchJobsIndexResponse200HitsItem']]): the jobs that matched the query
        hit_count (Union[Unset, float]): how many jobs matched in total
        index_metadata (Union[Unset, SearchJobsIndexResponse200IndexMetadata]): Metadata about the index current state
    """

    query_parse_errors: Union[Unset, List[str]] = UNSET
    hits: Union[Unset, List["SearchJobsIndexResponse200HitsItem"]] = UNSET
    hit_count: Union[Unset, float] = UNSET
    index_metadata: Union[Unset, "SearchJobsIndexResponse200IndexMetadata"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query_parse_errors: Union[Unset, List[str]] = UNSET
        if not isinstance(self.query_parse_errors, Unset):
            query_parse_errors = self.query_parse_errors

        hits: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.hits, Unset):
            hits = []
            for hits_item_data in self.hits:
                hits_item = hits_item_data.to_dict()

                hits.append(hits_item)

        hit_count = self.hit_count
        index_metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.index_metadata, Unset):
            index_metadata = self.index_metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if query_parse_errors is not UNSET:
            field_dict["query_parse_errors"] = query_parse_errors
        if hits is not UNSET:
            field_dict["hits"] = hits
        if hit_count is not UNSET:
            field_dict["hit_count"] = hit_count
        if index_metadata is not UNSET:
            field_dict["index_metadata"] = index_metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.search_jobs_index_response_200_hits_item import SearchJobsIndexResponse200HitsItem
        from ..models.search_jobs_index_response_200_index_metadata import SearchJobsIndexResponse200IndexMetadata

        d = src_dict.copy()
        query_parse_errors = cast(List[str], d.pop("query_parse_errors", UNSET))

        hits = []
        _hits = d.pop("hits", UNSET)
        for hits_item_data in _hits or []:
            hits_item = SearchJobsIndexResponse200HitsItem.from_dict(hits_item_data)

            hits.append(hits_item)

        hit_count = d.pop("hit_count", UNSET)

        _index_metadata = d.pop("index_metadata", UNSET)
        index_metadata: Union[Unset, SearchJobsIndexResponse200IndexMetadata]
        if isinstance(_index_metadata, Unset):
            index_metadata = UNSET
        else:
            index_metadata = SearchJobsIndexResponse200IndexMetadata.from_dict(_index_metadata)

        search_jobs_index_response_200 = cls(
            query_parse_errors=query_parse_errors,
            hits=hits,
            hit_count=hit_count,
            index_metadata=index_metadata,
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
