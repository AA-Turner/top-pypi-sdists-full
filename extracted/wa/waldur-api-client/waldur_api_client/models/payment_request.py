import datetime
from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="PaymentRequest")


@_attrs_define
class PaymentRequest:
    """
    Attributes:
        profile (str):
        date_of_payment (datetime.date):
        sum_ (Union[Unset, str]):
        proof (Union[File, None, Unset]):
    """

    profile: str
    date_of_payment: datetime.date
    sum_: Union[Unset, str] = UNSET
    proof: Union[File, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        profile = self.profile

        date_of_payment = self.date_of_payment.isoformat()

        sum_ = self.sum_

        proof: Union[None, Unset, types.FileTypes]
        if isinstance(self.proof, Unset):
            proof = UNSET
        elif isinstance(self.proof, File):
            proof = self.proof.to_tuple()

        else:
            proof = self.proof

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profile": profile,
                "date_of_payment": date_of_payment,
            }
        )
        if sum_ is not UNSET:
            field_dict["sum"] = sum_
        if proof is not UNSET:
            field_dict["proof"] = proof

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        profile = d.pop("profile")

        date_of_payment = isoparse(d.pop("date_of_payment")).date()

        sum_ = d.pop("sum", UNSET)

        def _parse_proof(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                proof_type_0 = File(payload=BytesIO(data))

                return proof_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        proof = _parse_proof(d.pop("proof", UNSET))

        payment_request = cls(
            profile=profile,
            date_of_payment=date_of_payment,
            sum_=sum_,
            proof=proof,
        )

        payment_request.additional_properties = d
        return payment_request

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
