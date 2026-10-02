from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewerSuggestionTopMatchingProposal")


@_attrs_define
class ReviewerSuggestionTopMatchingProposal:
    """
    Attributes:
        uuid (UUID):
        affinity (float):
        name (Union[Unset, str]):
        slug (Union[Unset, str]):
        keyword_score (Union[None, Unset, float]):
        text_score (Union[None, Unset, float]):
        has_coi (Union[None, Unset, bool]):
        coi_type (Union[None, Unset, str]):
        coi_severity (Union[None, Unset, str]):
    """

    uuid: UUID
    affinity: float
    name: Union[Unset, str] = UNSET
    slug: Union[Unset, str] = UNSET
    keyword_score: Union[None, Unset, float] = UNSET
    text_score: Union[None, Unset, float] = UNSET
    has_coi: Union[None, Unset, bool] = UNSET
    coi_type: Union[None, Unset, str] = UNSET
    coi_severity: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        affinity = self.affinity

        name = self.name

        slug = self.slug

        keyword_score: Union[None, Unset, float]
        if isinstance(self.keyword_score, Unset):
            keyword_score = UNSET
        else:
            keyword_score = self.keyword_score

        text_score: Union[None, Unset, float]
        if isinstance(self.text_score, Unset):
            text_score = UNSET
        else:
            text_score = self.text_score

        has_coi: Union[None, Unset, bool]
        if isinstance(self.has_coi, Unset):
            has_coi = UNSET
        else:
            has_coi = self.has_coi

        coi_type: Union[None, Unset, str]
        if isinstance(self.coi_type, Unset):
            coi_type = UNSET
        else:
            coi_type = self.coi_type

        coi_severity: Union[None, Unset, str]
        if isinstance(self.coi_severity, Unset):
            coi_severity = UNSET
        else:
            coi_severity = self.coi_severity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "affinity": affinity,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if slug is not UNSET:
            field_dict["slug"] = slug
        if keyword_score is not UNSET:
            field_dict["keyword_score"] = keyword_score
        if text_score is not UNSET:
            field_dict["text_score"] = text_score
        if has_coi is not UNSET:
            field_dict["has_coi"] = has_coi
        if coi_type is not UNSET:
            field_dict["coi_type"] = coi_type
        if coi_severity is not UNSET:
            field_dict["coi_severity"] = coi_severity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        affinity = d.pop("affinity")

        name = d.pop("name", UNSET)

        slug = d.pop("slug", UNSET)

        def _parse_keyword_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        keyword_score = _parse_keyword_score(d.pop("keyword_score", UNSET))

        def _parse_text_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        text_score = _parse_text_score(d.pop("text_score", UNSET))

        def _parse_has_coi(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        has_coi = _parse_has_coi(d.pop("has_coi", UNSET))

        def _parse_coi_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        coi_type = _parse_coi_type(d.pop("coi_type", UNSET))

        def _parse_coi_severity(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        coi_severity = _parse_coi_severity(d.pop("coi_severity", UNSET))

        reviewer_suggestion_top_matching_proposal = cls(
            uuid=uuid,
            affinity=affinity,
            name=name,
            slug=slug,
            keyword_score=keyword_score,
            text_score=text_score,
            has_coi=has_coi,
            coi_type=coi_type,
            coi_severity=coi_severity,
        )

        reviewer_suggestion_top_matching_proposal.additional_properties = d
        return reviewer_suggestion_top_matching_proposal

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
