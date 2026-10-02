from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.affinity_method_enum import AffinityMethodEnum
from ..models.matching_algorithm import MatchingAlgorithm
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedMatchingConfigurationRequest")


@_attrs_define
class PatchedMatchingConfigurationRequest:
    """
    Attributes:
        affinity_method (Union[Unset, AffinityMethodEnum]):
        keyword_weight (Union[Unset, float]):
        text_weight (Union[Unset, float]):
        min_reviewers_per_proposal (Union[Unset, int]):
        max_reviewers_per_proposal (Union[Unset, int]):
        min_proposals_per_reviewer (Union[Unset, int]):
        max_proposals_per_reviewer (Union[Unset, int]):
        algorithm (Union[Unset, MatchingAlgorithm]):
        min_affinity_threshold (Union[Unset, float]): Minimum affinity score for FairFlow algorithm
        use_reviewer_bids (Union[Unset, bool]):
        bid_weight (Union[Unset, float]):
    """

    affinity_method: Union[Unset, AffinityMethodEnum] = UNSET
    keyword_weight: Union[Unset, float] = UNSET
    text_weight: Union[Unset, float] = UNSET
    min_reviewers_per_proposal: Union[Unset, int] = UNSET
    max_reviewers_per_proposal: Union[Unset, int] = UNSET
    min_proposals_per_reviewer: Union[Unset, int] = UNSET
    max_proposals_per_reviewer: Union[Unset, int] = UNSET
    algorithm: Union[Unset, MatchingAlgorithm] = UNSET
    min_affinity_threshold: Union[Unset, float] = UNSET
    use_reviewer_bids: Union[Unset, bool] = UNSET
    bid_weight: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        affinity_method: Union[Unset, str] = UNSET
        if not isinstance(self.affinity_method, Unset):
            affinity_method = self.affinity_method.value

        keyword_weight = self.keyword_weight

        text_weight = self.text_weight

        min_reviewers_per_proposal = self.min_reviewers_per_proposal

        max_reviewers_per_proposal = self.max_reviewers_per_proposal

        min_proposals_per_reviewer = self.min_proposals_per_reviewer

        max_proposals_per_reviewer = self.max_proposals_per_reviewer

        algorithm: Union[Unset, str] = UNSET
        if not isinstance(self.algorithm, Unset):
            algorithm = self.algorithm.value

        min_affinity_threshold = self.min_affinity_threshold

        use_reviewer_bids = self.use_reviewer_bids

        bid_weight = self.bid_weight

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if affinity_method is not UNSET:
            field_dict["affinity_method"] = affinity_method
        if keyword_weight is not UNSET:
            field_dict["keyword_weight"] = keyword_weight
        if text_weight is not UNSET:
            field_dict["text_weight"] = text_weight
        if min_reviewers_per_proposal is not UNSET:
            field_dict["min_reviewers_per_proposal"] = min_reviewers_per_proposal
        if max_reviewers_per_proposal is not UNSET:
            field_dict["max_reviewers_per_proposal"] = max_reviewers_per_proposal
        if min_proposals_per_reviewer is not UNSET:
            field_dict["min_proposals_per_reviewer"] = min_proposals_per_reviewer
        if max_proposals_per_reviewer is not UNSET:
            field_dict["max_proposals_per_reviewer"] = max_proposals_per_reviewer
        if algorithm is not UNSET:
            field_dict["algorithm"] = algorithm
        if min_affinity_threshold is not UNSET:
            field_dict["min_affinity_threshold"] = min_affinity_threshold
        if use_reviewer_bids is not UNSET:
            field_dict["use_reviewer_bids"] = use_reviewer_bids
        if bid_weight is not UNSET:
            field_dict["bid_weight"] = bid_weight

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _affinity_method = d.pop("affinity_method", UNSET)
        affinity_method: Union[Unset, AffinityMethodEnum]
        if isinstance(_affinity_method, Unset):
            affinity_method = UNSET
        else:
            affinity_method = AffinityMethodEnum(_affinity_method)

        keyword_weight = d.pop("keyword_weight", UNSET)

        text_weight = d.pop("text_weight", UNSET)

        min_reviewers_per_proposal = d.pop("min_reviewers_per_proposal", UNSET)

        max_reviewers_per_proposal = d.pop("max_reviewers_per_proposal", UNSET)

        min_proposals_per_reviewer = d.pop("min_proposals_per_reviewer", UNSET)

        max_proposals_per_reviewer = d.pop("max_proposals_per_reviewer", UNSET)

        _algorithm = d.pop("algorithm", UNSET)
        algorithm: Union[Unset, MatchingAlgorithm]
        if isinstance(_algorithm, Unset):
            algorithm = UNSET
        else:
            algorithm = MatchingAlgorithm(_algorithm)

        min_affinity_threshold = d.pop("min_affinity_threshold", UNSET)

        use_reviewer_bids = d.pop("use_reviewer_bids", UNSET)

        bid_weight = d.pop("bid_weight", UNSET)

        patched_matching_configuration_request = cls(
            affinity_method=affinity_method,
            keyword_weight=keyword_weight,
            text_weight=text_weight,
            min_reviewers_per_proposal=min_reviewers_per_proposal,
            max_reviewers_per_proposal=max_reviewers_per_proposal,
            min_proposals_per_reviewer=min_proposals_per_reviewer,
            max_proposals_per_reviewer=max_proposals_per_reviewer,
            algorithm=algorithm,
            min_affinity_threshold=min_affinity_threshold,
            use_reviewer_bids=use_reviewer_bids,
            bid_weight=bid_weight,
        )

        patched_matching_configuration_request.additional_properties = d
        return patched_matching_configuration_request

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
