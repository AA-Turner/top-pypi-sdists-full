import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.bid_enum import BidEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewerBid")


@_attrs_define
class ReviewerBid:
    """
    Attributes:
        uuid (UUID):
        call (str):
        call_uuid (UUID):
        reviewer (str):
        reviewer_uuid (UUID):
        reviewer_name (str):
        proposal (str):
        proposal_uuid (UUID):
        proposal_name (str):
        bid (BidEnum):
        bid_display (str):
        submitted_at (datetime.datetime):
        modified_at (datetime.datetime):
        comment (Union[Unset, str]): Optional comment explaining the bid
    """

    uuid: UUID
    call: str
    call_uuid: UUID
    reviewer: str
    reviewer_uuid: UUID
    reviewer_name: str
    proposal: str
    proposal_uuid: UUID
    proposal_name: str
    bid: BidEnum
    bid_display: str
    submitted_at: datetime.datetime
    modified_at: datetime.datetime
    comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        call = self.call

        call_uuid = str(self.call_uuid)

        reviewer = self.reviewer

        reviewer_uuid = str(self.reviewer_uuid)

        reviewer_name = self.reviewer_name

        proposal = self.proposal

        proposal_uuid = str(self.proposal_uuid)

        proposal_name = self.proposal_name

        bid = self.bid.value

        bid_display = self.bid_display

        submitted_at = self.submitted_at.isoformat()

        modified_at = self.modified_at.isoformat()

        comment = self.comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "call": call,
                "call_uuid": call_uuid,
                "reviewer": reviewer,
                "reviewer_uuid": reviewer_uuid,
                "reviewer_name": reviewer_name,
                "proposal": proposal,
                "proposal_uuid": proposal_uuid,
                "proposal_name": proposal_name,
                "bid": bid,
                "bid_display": bid_display,
                "submitted_at": submitted_at,
                "modified_at": modified_at,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        call = d.pop("call")

        call_uuid = UUID(d.pop("call_uuid"))

        reviewer = d.pop("reviewer")

        reviewer_uuid = UUID(d.pop("reviewer_uuid"))

        reviewer_name = d.pop("reviewer_name")

        proposal = d.pop("proposal")

        proposal_uuid = UUID(d.pop("proposal_uuid"))

        proposal_name = d.pop("proposal_name")

        bid = BidEnum(d.pop("bid"))

        bid_display = d.pop("bid_display")

        submitted_at = isoparse(d.pop("submitted_at"))

        modified_at = isoparse(d.pop("modified_at"))

        comment = d.pop("comment", UNSET)

        reviewer_bid = cls(
            uuid=uuid,
            call=call,
            call_uuid=call_uuid,
            reviewer=reviewer,
            reviewer_uuid=reviewer_uuid,
            reviewer_name=reviewer_name,
            proposal=proposal,
            proposal_uuid=proposal_uuid,
            proposal_name=proposal_name,
            bid=bid,
            bid_display=bid_display,
            submitted_at=submitted_at,
            modified_at=modified_at,
            comment=comment,
        )

        reviewer_bid.additional_properties = d
        return reviewer_bid

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
