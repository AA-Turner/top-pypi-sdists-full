from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.allocation_candidates_response_provider_summaries_additional_property import (
        AllocationCandidatesResponseProviderSummariesAdditionalProperty,
    )


T = TypeVar("T", bound="AllocationCandidatesResponseProviderSummaries")


@_attrs_define
class AllocationCandidatesResponseProviderSummaries:
    """Placement's per-provider summary: maps resource_provider_uuid → {resources: {CLASS: {used, capacity}, ...}, traits:
    [...]}.

    """

    additional_properties: dict[str, "AllocationCandidatesResponseProviderSummariesAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.allocation_candidates_response_provider_summaries_additional_property import (
            AllocationCandidatesResponseProviderSummariesAdditionalProperty,
        )

        d = dict(src_dict)
        allocation_candidates_response_provider_summaries = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = AllocationCandidatesResponseProviderSummariesAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        allocation_candidates_response_provider_summaries.additional_properties = additional_properties
        return allocation_candidates_response_provider_summaries

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "AllocationCandidatesResponseProviderSummariesAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "AllocationCandidatesResponseProviderSummariesAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
