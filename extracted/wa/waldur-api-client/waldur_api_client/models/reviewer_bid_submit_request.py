from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.bid_enum import BidEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewerBidSubmitRequest")


@_attrs_define
class ReviewerBidSubmitRequest:
    """
    Attributes:
        proposal_uuid (UUID):
        bid (BidEnum):
        comment (Union[Unset, str]):  Default: ''.
    """

    proposal_uuid: UUID
    bid: BidEnum
    comment: Union[Unset, str] = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        proposal_uuid = str(self.proposal_uuid)

        bid = self.bid.value

        comment = self.comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "proposal_uuid": proposal_uuid,
                "bid": bid,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        proposal_uuid = UUID(d.pop("proposal_uuid"))

        bid = BidEnum(d.pop("bid"))

        comment = d.pop("comment", UNSET)

        reviewer_bid_submit_request = cls(
            proposal_uuid=proposal_uuid,
            bid=bid,
            comment=comment,
        )

        reviewer_bid_submit_request.additional_properties = d
        return reviewer_bid_submit_request

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
