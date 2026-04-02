from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.generate_suggestions_request_source_enum import GenerateSuggestionsRequestSourceEnum
from ..models.keyword_search_mode_enum import KeywordSearchModeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="GenerateSuggestionsRequestRequest")


@_attrs_define
class GenerateSuggestionsRequestRequest:
    """
    Attributes:
        source (Union[Unset, GenerateSuggestionsRequestSourceEnum]):  Default:
            GenerateSuggestionsRequestSourceEnum.ALL_PROPOSALS.
        proposal_uuids (Union[Unset, list[UUID]]): Specific proposal UUIDs to match against (for selected_proposals
            source)
        keywords (Union[Unset, list[str]]): Custom keywords to search for (for custom_keywords source)
        keyword_search_mode (Union[Unset, KeywordSearchModeEnum]):  Default: KeywordSearchModeEnum.EXPERTISE_ONLY.
        min_affinity_threshold (Union[Unset, float]): Minimum affinity score for suggestions (0.0-1.0)
    """

    source: Union[Unset, GenerateSuggestionsRequestSourceEnum] = GenerateSuggestionsRequestSourceEnum.ALL_PROPOSALS
    proposal_uuids: Union[Unset, list[UUID]] = UNSET
    keywords: Union[Unset, list[str]] = UNSET
    keyword_search_mode: Union[Unset, KeywordSearchModeEnum] = KeywordSearchModeEnum.EXPERTISE_ONLY
    min_affinity_threshold: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        proposal_uuids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.proposal_uuids, Unset):
            proposal_uuids = []
            for proposal_uuids_item_data in self.proposal_uuids:
                proposal_uuids_item = str(proposal_uuids_item_data)
                proposal_uuids.append(proposal_uuids_item)

        keywords: Union[Unset, list[str]] = UNSET
        if not isinstance(self.keywords, Unset):
            keywords = self.keywords

        keyword_search_mode: Union[Unset, str] = UNSET
        if not isinstance(self.keyword_search_mode, Unset):
            keyword_search_mode = self.keyword_search_mode.value

        min_affinity_threshold = self.min_affinity_threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if source is not UNSET:
            field_dict["source"] = source
        if proposal_uuids is not UNSET:
            field_dict["proposal_uuids"] = proposal_uuids
        if keywords is not UNSET:
            field_dict["keywords"] = keywords
        if keyword_search_mode is not UNSET:
            field_dict["keyword_search_mode"] = keyword_search_mode
        if min_affinity_threshold is not UNSET:
            field_dict["min_affinity_threshold"] = min_affinity_threshold

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _source = d.pop("source", UNSET)
        source: Union[Unset, GenerateSuggestionsRequestSourceEnum]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = GenerateSuggestionsRequestSourceEnum(_source)

        proposal_uuids = []
        _proposal_uuids = d.pop("proposal_uuids", UNSET)
        for proposal_uuids_item_data in _proposal_uuids or []:
            proposal_uuids_item = UUID(proposal_uuids_item_data)

            proposal_uuids.append(proposal_uuids_item)

        keywords = cast(list[str], d.pop("keywords", UNSET))

        _keyword_search_mode = d.pop("keyword_search_mode", UNSET)
        keyword_search_mode: Union[Unset, KeywordSearchModeEnum]
        if isinstance(_keyword_search_mode, Unset):
            keyword_search_mode = UNSET
        else:
            keyword_search_mode = KeywordSearchModeEnum(_keyword_search_mode)

        min_affinity_threshold = d.pop("min_affinity_threshold", UNSET)

        generate_suggestions_request_request = cls(
            source=source,
            proposal_uuids=proposal_uuids,
            keywords=keywords,
            keyword_search_mode=keyword_search_mode,
            min_affinity_threshold=min_affinity_threshold,
        )

        generate_suggestions_request_request.additional_properties = d
        return generate_suggestions_request_request

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
