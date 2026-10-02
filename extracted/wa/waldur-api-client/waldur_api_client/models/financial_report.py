import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_price_estimate import NestedPriceEstimate
    from ..models.payment_profile import PaymentProfile


T = TypeVar("T", bound="FinancialReport")


@_attrs_define
class FinancialReport:
    """
    Attributes:
        name (str):
        uuid (UUID):
        created (datetime.datetime):
        payment_profiles (list['PaymentProfile']):
        billing_price_estimate (NestedPriceEstimate):
        abbreviation (Union[Unset, str]):
        accounting_start_date (Union[Unset, datetime.datetime]):
        registration_code (Union[Unset, str]):
        agreement_number (Union[Unset, str]):
    """

    name: str
    uuid: UUID
    created: datetime.datetime
    payment_profiles: list["PaymentProfile"]
    billing_price_estimate: "NestedPriceEstimate"
    abbreviation: Union[Unset, str] = UNSET
    accounting_start_date: Union[Unset, datetime.datetime] = UNSET
    registration_code: Union[Unset, str] = UNSET
    agreement_number: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        uuid = str(self.uuid)

        created = self.created.isoformat()

        payment_profiles = []
        for payment_profiles_item_data in self.payment_profiles:
            payment_profiles_item = payment_profiles_item_data.to_dict()
            payment_profiles.append(payment_profiles_item)

        billing_price_estimate = self.billing_price_estimate.to_dict()

        abbreviation = self.abbreviation

        accounting_start_date: Union[Unset, str] = UNSET
        if not isinstance(self.accounting_start_date, Unset):
            accounting_start_date = self.accounting_start_date.isoformat()

        registration_code = self.registration_code

        agreement_number = self.agreement_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "uuid": uuid,
                "created": created,
                "payment_profiles": payment_profiles,
                "billing_price_estimate": billing_price_estimate,
            }
        )
        if abbreviation is not UNSET:
            field_dict["abbreviation"] = abbreviation
        if accounting_start_date is not UNSET:
            field_dict["accounting_start_date"] = accounting_start_date
        if registration_code is not UNSET:
            field_dict["registration_code"] = registration_code
        if agreement_number is not UNSET:
            field_dict["agreement_number"] = agreement_number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_price_estimate import NestedPriceEstimate
        from ..models.payment_profile import PaymentProfile

        d = dict(src_dict)
        name = d.pop("name")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        payment_profiles = []
        _payment_profiles = d.pop("payment_profiles")
        for payment_profiles_item_data in _payment_profiles:
            payment_profiles_item = PaymentProfile.from_dict(payment_profiles_item_data)

            payment_profiles.append(payment_profiles_item)

        billing_price_estimate = NestedPriceEstimate.from_dict(d.pop("billing_price_estimate"))

        abbreviation = d.pop("abbreviation", UNSET)

        _accounting_start_date = d.pop("accounting_start_date", UNSET)
        accounting_start_date: Union[Unset, datetime.datetime]
        if isinstance(_accounting_start_date, Unset):
            accounting_start_date = UNSET
        else:
            accounting_start_date = isoparse(_accounting_start_date)

        registration_code = d.pop("registration_code", UNSET)

        agreement_number = d.pop("agreement_number", UNSET)

        financial_report = cls(
            name=name,
            uuid=uuid,
            created=created,
            payment_profiles=payment_profiles,
            billing_price_estimate=billing_price_estimate,
            abbreviation=abbreviation,
            accounting_start_date=accounting_start_date,
            registration_code=registration_code,
            agreement_number=agreement_number,
        )

        financial_report.additional_properties = d
        return financial_report

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
