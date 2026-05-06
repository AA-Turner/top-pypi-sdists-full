from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.allocation_candidates_response_provider_summaries import AllocationCandidatesResponseProviderSummaries


T = TypeVar("T", bound="AllocationCandidatesResponse")


@_attrs_define
class AllocationCandidatesResponse:
    """
    Attributes:
        candidate_count (int): Total number of allocation candidates Placement returned.
        provider_summaries (AllocationCandidatesResponseProviderSummaries): Placement's per-provider summary: maps
            resource_provider_uuid → {resources: {CLASS: {used, capacity}, ...}, traits: [...]}.
    """

    candidate_count: int
    provider_summaries: "AllocationCandidatesResponseProviderSummaries"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        candidate_count = self.candidate_count

        provider_summaries = self.provider_summaries.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "candidate_count": candidate_count,
                "provider_summaries": provider_summaries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.allocation_candidates_response_provider_summaries import (
            AllocationCandidatesResponseProviderSummaries,
        )

        d = dict(src_dict)
        candidate_count = d.pop("candidate_count")

        provider_summaries = AllocationCandidatesResponseProviderSummaries.from_dict(d.pop("provider_summaries"))

        allocation_candidates_response = cls(
            candidate_count=candidate_count,
            provider_summaries=provider_summaries,
        )

        allocation_candidates_response.additional_properties = d
        return allocation_candidates_response

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
