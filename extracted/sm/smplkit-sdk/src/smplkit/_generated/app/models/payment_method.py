from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.payment_method_billing_details import PaymentMethodBillingDetails


T = TypeVar("T", bound="PaymentMethod")


@_attrs_define
class PaymentMethod:
    """A saved card on file for the account, used to charge subscription
    invoices.

    The default payment method is changed via the `set_default` action
    rather than by updating this field through PUT.

        Example:
            {'billing_details': {'address': {'city': 'Leesburg', 'country': 'US', 'line1': '123 Main St', 'postal_code':
                '20175', 'state': 'VA'}, 'email': 'jane@example.com', 'name': 'Jane Doe'}, 'brand': 'visa', 'created_at':
                '2026-04-23T12:34:56Z', 'default': True, 'exp_month': 8, 'exp_year': 2028, 'last4': '4242', 'updated_at':
                '2026-04-23T12:34:56Z'}

        Attributes:
            brand (None | str | Unset): Card network brand, e.g. `visa`, `mastercard`, `amex`.
            last4 (None | str | Unset): Last four digits of the card number.
            exp_month (int | None | Unset): Expiry month (1-12).
            exp_year (int | None | Unset): Expiry year (four-digit).
            default (bool | None | Unset): Whether this payment method is the account's default for subscription charges.
                Use the `set_default` action to change which payment method is default — this field is not writable via PUT.
            billing_details (None | PaymentMethodBillingDetails | Unset): Billing details (name, email, phone, address)
                associated with the card.
            created_at (datetime.datetime | None | Unset): When the payment method was registered.
            updated_at (datetime.datetime | None | Unset): When the payment method was last modified.
    """

    brand: None | str | Unset = UNSET
    last4: None | str | Unset = UNSET
    exp_month: int | None | Unset = UNSET
    exp_year: int | None | Unset = UNSET
    default: bool | None | Unset = UNSET
    billing_details: None | PaymentMethodBillingDetails | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.payment_method_billing_details import PaymentMethodBillingDetails

        brand: None | str | Unset
        if isinstance(self.brand, Unset):
            brand = UNSET
        else:
            brand = self.brand

        last4: None | str | Unset
        if isinstance(self.last4, Unset):
            last4 = UNSET
        else:
            last4 = self.last4

        exp_month: int | None | Unset
        if isinstance(self.exp_month, Unset):
            exp_month = UNSET
        else:
            exp_month = self.exp_month

        exp_year: int | None | Unset
        if isinstance(self.exp_year, Unset):
            exp_year = UNSET
        else:
            exp_year = self.exp_year

        default: bool | None | Unset
        if isinstance(self.default, Unset):
            default = UNSET
        else:
            default = self.default

        billing_details: dict[str, Any] | None | Unset
        if isinstance(self.billing_details, Unset):
            billing_details = UNSET
        elif isinstance(self.billing_details, PaymentMethodBillingDetails):
            billing_details = self.billing_details.to_dict()
        else:
            billing_details = self.billing_details

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if brand is not UNSET:
            field_dict["brand"] = brand
        if last4 is not UNSET:
            field_dict["last4"] = last4
        if exp_month is not UNSET:
            field_dict["exp_month"] = exp_month
        if exp_year is not UNSET:
            field_dict["exp_year"] = exp_year
        if default is not UNSET:
            field_dict["default"] = default
        if billing_details is not UNSET:
            field_dict["billing_details"] = billing_details
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.payment_method_billing_details import PaymentMethodBillingDetails

        d = dict(src_dict)

        def _parse_brand(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        brand = _parse_brand(d.pop("brand", UNSET))

        def _parse_last4(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last4 = _parse_last4(d.pop("last4", UNSET))

        def _parse_exp_month(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        exp_month = _parse_exp_month(d.pop("exp_month", UNSET))

        def _parse_exp_year(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        exp_year = _parse_exp_year(d.pop("exp_year", UNSET))

        def _parse_default(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        default = _parse_default(d.pop("default", UNSET))

        def _parse_billing_details(data: object) -> None | PaymentMethodBillingDetails | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                billing_details_type_0 = PaymentMethodBillingDetails.from_dict(data)

                return billing_details_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PaymentMethodBillingDetails | Unset, data)

        billing_details = _parse_billing_details(d.pop("billing_details", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        payment_method = cls(
            brand=brand,
            last4=last4,
            exp_month=exp_month,
            exp_year=exp_year,
            default=default,
            billing_details=billing_details,
            created_at=created_at,
            updated_at=updated_at,
        )

        payment_method.additional_properties = d
        return payment_method

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
