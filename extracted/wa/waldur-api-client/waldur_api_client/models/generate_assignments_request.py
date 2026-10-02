from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GenerateAssignmentsRequest")


@_attrs_define
class GenerateAssignmentsRequest:
    """
    Attributes:
        proposal_uuids (Union[Unset, list[UUID]]): Specific proposal UUIDs to generate assignments for. If empty,
            generates for all submitted proposals needing reviewers.
        reviewers_per_proposal (Union[Unset, int]): Number of reviewers to assign per proposal. If not specified, uses
            call's minimum_number_of_reviewers setting.
    """

    proposal_uuids: Union[Unset, list[UUID]] = UNSET
    reviewers_per_proposal: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        proposal_uuids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.proposal_uuids, Unset):
            proposal_uuids = []
            for proposal_uuids_item_data in self.proposal_uuids:
                proposal_uuids_item = str(proposal_uuids_item_data)
                proposal_uuids.append(proposal_uuids_item)

        reviewers_per_proposal = self.reviewers_per_proposal

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if proposal_uuids is not UNSET:
            field_dict["proposal_uuids"] = proposal_uuids
        if reviewers_per_proposal is not UNSET:
            field_dict["reviewers_per_proposal"] = reviewers_per_proposal

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        proposal_uuids = []
        _proposal_uuids = d.pop("proposal_uuids", UNSET)
        for proposal_uuids_item_data in _proposal_uuids or []:
            proposal_uuids_item = UUID(proposal_uuids_item_data)

            proposal_uuids.append(proposal_uuids_item)

        reviewers_per_proposal = d.pop("reviewers_per_proposal", UNSET)

        generate_assignments_request = cls(
            proposal_uuids=proposal_uuids,
            reviewers_per_proposal=reviewers_per_proposal,
        )

        generate_assignments_request.additional_properties = d
        return generate_assignments_request

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
