from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RoundReviewer")


@_attrs_define
class RoundReviewer:
    """
    Attributes:
        full_name (str):
        email (str):
        accepted_proposals (int):
        rejected_proposals (int):
        in_review_proposals (int):
    """

    full_name: str
    email: str
    accepted_proposals: int
    rejected_proposals: int
    in_review_proposals: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        full_name = self.full_name

        email = self.email

        accepted_proposals = self.accepted_proposals

        rejected_proposals = self.rejected_proposals

        in_review_proposals = self.in_review_proposals

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "full_name": full_name,
                "email": email,
                "accepted_proposals": accepted_proposals,
                "rejected_proposals": rejected_proposals,
                "in_review_proposals": in_review_proposals,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        full_name = d.pop("full_name")

        email = d.pop("email")

        accepted_proposals = d.pop("accepted_proposals")

        rejected_proposals = d.pop("rejected_proposals")

        in_review_proposals = d.pop("in_review_proposals")

        round_reviewer = cls(
            full_name=full_name,
            email=email,
            accepted_proposals=accepted_proposals,
            rejected_proposals=rejected_proposals,
            in_review_proposals=in_review_proposals,
        )

        round_reviewer.additional_properties = d
        return round_reviewer

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
