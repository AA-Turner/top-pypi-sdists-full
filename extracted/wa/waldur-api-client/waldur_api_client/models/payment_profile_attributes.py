from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentProfileAttributes")


@_attrs_define
class PaymentProfileAttributes:
    """
    Attributes:
        end_date (Union[Unset, str]):
        agreement_number (Union[Unset, str]):
        contract_sum (Union[Unset, int]):
    """

    end_date: Union[Unset, str] = UNSET
    agreement_number: Union[Unset, str] = UNSET
    contract_sum: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        end_date = self.end_date

        agreement_number = self.agreement_number

        contract_sum = self.contract_sum

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if agreement_number is not UNSET:
            field_dict["agreement_number"] = agreement_number
        if contract_sum is not UNSET:
            field_dict["contract_sum"] = contract_sum

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        end_date = d.pop("end_date", UNSET)

        agreement_number = d.pop("agreement_number", UNSET)

        contract_sum = d.pop("contract_sum", UNSET)

        payment_profile_attributes = cls(
            end_date=end_date,
            agreement_number=agreement_number,
            contract_sum=contract_sum,
        )

        payment_profile_attributes.additional_properties = d
        return payment_profile_attributes

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
