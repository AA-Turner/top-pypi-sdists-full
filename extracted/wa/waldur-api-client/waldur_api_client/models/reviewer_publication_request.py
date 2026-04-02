from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.venue_type_enum import VenueTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewerPublicationRequest")


@_attrs_define
class ReviewerPublicationRequest:
    """
    Attributes:
        title (str):
        publication_year (int):
        venue (str): Journal or conference name
        doi (Union[None, Unset, str]): Digital Object Identifier
        venue_type (Union[Unset, VenueTypeEnum]):
        abstract (Union[Unset, str]):
        coauthors (Union[Unset, Any]): List of co-author names and identifiers
        external_ids (Union[Unset, Any]): External identifiers: {"semantic_scholar": "...", "pubmed": "..."}
        is_excluded_from_matching (Union[Unset, bool]): User can exclude old papers from expertise matching
    """

    title: str
    publication_year: int
    venue: str
    doi: Union[None, Unset, str] = UNSET
    venue_type: Union[Unset, VenueTypeEnum] = UNSET
    abstract: Union[Unset, str] = UNSET
    coauthors: Union[Unset, Any] = UNSET
    external_ids: Union[Unset, Any] = UNSET
    is_excluded_from_matching: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        publication_year = self.publication_year

        venue = self.venue

        doi: Union[None, Unset, str]
        if isinstance(self.doi, Unset):
            doi = UNSET
        else:
            doi = self.doi

        venue_type: Union[Unset, str] = UNSET
        if not isinstance(self.venue_type, Unset):
            venue_type = self.venue_type.value

        abstract = self.abstract

        coauthors = self.coauthors

        external_ids = self.external_ids

        is_excluded_from_matching = self.is_excluded_from_matching

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "publication_year": publication_year,
                "venue": venue,
            }
        )
        if doi is not UNSET:
            field_dict["doi"] = doi
        if venue_type is not UNSET:
            field_dict["venue_type"] = venue_type
        if abstract is not UNSET:
            field_dict["abstract"] = abstract
        if coauthors is not UNSET:
            field_dict["coauthors"] = coauthors
        if external_ids is not UNSET:
            field_dict["external_ids"] = external_ids
        if is_excluded_from_matching is not UNSET:
            field_dict["is_excluded_from_matching"] = is_excluded_from_matching

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        publication_year = d.pop("publication_year")

        venue = d.pop("venue")

        def _parse_doi(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        doi = _parse_doi(d.pop("doi", UNSET))

        _venue_type = d.pop("venue_type", UNSET)
        venue_type: Union[Unset, VenueTypeEnum]
        if isinstance(_venue_type, Unset):
            venue_type = UNSET
        else:
            venue_type = VenueTypeEnum(_venue_type)

        abstract = d.pop("abstract", UNSET)

        coauthors = d.pop("coauthors", UNSET)

        external_ids = d.pop("external_ids", UNSET)

        is_excluded_from_matching = d.pop("is_excluded_from_matching", UNSET)

        reviewer_publication_request = cls(
            title=title,
            publication_year=publication_year,
            venue=venue,
            doi=doi,
            venue_type=venue_type,
            abstract=abstract,
            coauthors=coauthors,
            external_ids=external_ids,
            is_excluded_from_matching=is_excluded_from_matching,
        )

        reviewer_publication_request.additional_properties = d
        return reviewer_publication_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
