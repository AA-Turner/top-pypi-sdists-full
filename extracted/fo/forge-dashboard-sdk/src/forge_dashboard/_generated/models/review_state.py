from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.review_state_decision import ReviewStateDecision






T = TypeVar("T", bound="ReviewState")



@_attrs_define
class ReviewState:
    """ Where a pull request stands on code review. The whole object is
    omitted when the owning forge couldn't report it (a Forgejo
    reviews call that failed, a draft Forgejo pull request this
    service doesn't spend a call on), so a missing "review" means
    "unknown" and never "nobody reviewed it."

    GitHub: read from fields on the existing GraphQL query
    (reviewDecision, reviewRequests, latestReviews), so it adds no
    per-pull-request requests. Forgejo: requestedReviewers comes free
    on the pull request list, but approvals and the decision need one
    reviews call per open, non-draft pull request, cached until that
    pull request's updatedAt changes.

        Attributes:
            decision (ReviewStateDecision): "approved" and "changes_requested" mean what they say.
                "review_required" means a review is still outstanding: GitHub
                says so itself when branch protection requires one, and on
                Forgejo it means reviewers are requested and nobody has
                approved. "none" means no review activity and nothing
                required or requested.
            approvals (int): Reviewers whose latest review is an approval. GitHub counts
                at most the 10 most recent reviewers.
            requested_reviewers (int): Users and teams still asked to review.
     """

    decision: ReviewStateDecision
    approvals: int
    requested_reviewers: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        decision = self.decision.value

        approvals = self.approvals

        requested_reviewers = self.requested_reviewers


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "decision": decision,
            "approvals": approvals,
            "requestedReviewers": requested_reviewers,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        decision = ReviewStateDecision(d.pop("decision"))




        approvals = d.pop("approvals")

        requested_reviewers = d.pop("requestedReviewers")

        review_state = cls(
            decision=decision,
            approvals=approvals,
            requested_reviewers=requested_reviewers,
        )


        review_state.additional_properties = d
        return review_state

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
