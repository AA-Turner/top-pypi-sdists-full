from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.bid_enum import BidEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedReviewerBidRequest")


@_attrs_define
class PatchedReviewerBidRequest:
    """
    Attributes:
        proposal (Union[Unset, str]):
        bid (Union[Unset, BidEnum]):
        comment (Union[Unset, str]): Optional comment explaining the bid
    """

    proposal: Union[Unset, str] = UNSET
    bid: Union[Unset, BidEnum] = UNSET
    comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        proposal = self.proposal

        bid: Union[Unset, str] = UNSET
        if not isinstance(self.bid, Unset):
            bid = self.bid.value

        comment = self.comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if proposal is not UNSET:
            field_dict["proposal"] = proposal
        if bid is not UNSET:
            field_dict["bid"] = bid
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        proposal = d.pop("proposal", UNSET)

        _bid = d.pop("bid", UNSET)
        bid: Union[Unset, BidEnum]
        if isinstance(_bid, Unset):
            bid = UNSET
        else:
            bid = BidEnum(_bid)

        comment = d.pop("comment", UNSET)

        patched_reviewer_bid_request = cls(
            proposal=proposal,
            bid=bid,
            comment=comment,
        )

        patched_reviewer_bid_request.additional_properties = d
        return patched_reviewer_bid_request

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
