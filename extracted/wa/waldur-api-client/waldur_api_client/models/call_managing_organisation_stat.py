from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CallManagingOrganisationStat")


@_attrs_define
class CallManagingOrganisationStat:
    """
    Attributes:
        open_calls (int):
        active_rounds (int):
        accepted_proposals (int):
        pending_proposals (int):
        pending_review (int):
        rounds_closing_in_one_week (int):
        calls_closing_in_one_week (int):
        offering_requests_pending (int):
    """

    open_calls: int
    active_rounds: int
    accepted_proposals: int
    pending_proposals: int
    pending_review: int
    rounds_closing_in_one_week: int
    calls_closing_in_one_week: int
    offering_requests_pending: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        open_calls = self.open_calls

        active_rounds = self.active_rounds

        accepted_proposals = self.accepted_proposals

        pending_proposals = self.pending_proposals

        pending_review = self.pending_review

        rounds_closing_in_one_week = self.rounds_closing_in_one_week

        calls_closing_in_one_week = self.calls_closing_in_one_week

        offering_requests_pending = self.offering_requests_pending

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "open_calls": open_calls,
                "active_rounds": active_rounds,
                "accepted_proposals": accepted_proposals,
                "pending_proposals": pending_proposals,
                "pending_review": pending_review,
                "rounds_closing_in_one_week": rounds_closing_in_one_week,
                "calls_closing_in_one_week": calls_closing_in_one_week,
                "offering_requests_pending": offering_requests_pending,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        open_calls = d.pop("open_calls")

        active_rounds = d.pop("active_rounds")

        accepted_proposals = d.pop("accepted_proposals")

        pending_proposals = d.pop("pending_proposals")

        pending_review = d.pop("pending_review")

        rounds_closing_in_one_week = d.pop("rounds_closing_in_one_week")

        calls_closing_in_one_week = d.pop("calls_closing_in_one_week")

        offering_requests_pending = d.pop("offering_requests_pending")

        call_managing_organisation_stat = cls(
            open_calls=open_calls,
            active_rounds=active_rounds,
            accepted_proposals=accepted_proposals,
            pending_proposals=pending_proposals,
            pending_review=pending_review,
            rounds_closing_in_one_week=rounds_closing_in_one_week,
            calls_closing_in_one_week=calls_closing_in_one_week,
            offering_requests_pending=offering_requests_pending,
        )

        call_managing_organisation_stat.additional_properties = d
        return call_managing_organisation_stat

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
