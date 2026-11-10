from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreditTopUpRequest")


@_attrs_define
class CreditTopUpRequest:
    """
    Attributes:
        amount (str): Positive to record a prepayment, negative to reverse one.
        comment (str):
        payment_reference (Union[Unset, str]): Bank transfer or payment identifier, kept in the ledger comment.
    """

    amount: str
    comment: str
    payment_reference: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        comment = self.comment

        payment_reference = self.payment_reference

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "comment": comment,
            }
        )
        if payment_reference is not UNSET:
            field_dict["payment_reference"] = payment_reference

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount = d.pop("amount")

        comment = d.pop("comment")

        payment_reference = d.pop("payment_reference", UNSET)

        credit_top_up_request = cls(
            amount=amount,
            comment=comment,
            payment_reference=payment_reference,
        )

        credit_top_up_request.additional_properties = d
        return credit_top_up_request

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
