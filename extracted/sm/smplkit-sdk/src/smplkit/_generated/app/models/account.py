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
    from ..models.account_product_subscriptions import AccountProductSubscriptions


T = TypeVar("T", bound="Account")


@_attrs_define
class Account:
    """A tenant of smplkit — the unit of isolation that owns all of a
    customer's resources (environments, contexts, API keys, and so on).

        Example:
            {'created_at': '2026-03-20T11:02:16.616Z', 'has_stripe_customer': False, 'key': 'acme_corp', 'name': 'Acme
                Corp'}

        Attributes:
            name (str): Human-readable name for the account.
            key (None | str | Unset): Stable URL-safe identifier for the account, derived from the account name at creation.
                Used in console URLs and other places that prefer a human-readable handle.
            has_stripe_customer (bool | Unset): `true` once the account has been linked to a billing provider customer
                record. Default: False.
            expires_at (datetime.datetime | None | Unset): When the account is scheduled to expire. `null` for accounts with
                no expiry.
            created_at (datetime.datetime | None | Unset): When the account was created.
            deleted_at (datetime.datetime | None | Unset): When the account was deleted. `null` for active accounts.
            product_subscriptions (AccountProductSubscriptions | None | Unset): Map of product key to the account's
                subscription summary for that product, including plan, status, and entitlement limits.
            entry_point (None | str | Unset): How the account first reached smplkit (e.g. `LOGIN`, `GET_STARTED`,
                `LIVE_DEMO`).
            show_sample_data (bool | None | Unset): Whether the account is currently configured to display the sample
                dataset alongside the customer's own resources.
            discount_override_pct (int | None | Unset): Custom discount percentage applied to the account in place of the
                volume-based discount schedule. `null` means the volume schedule applies. Who set it, when, and why are captured
                in the audit-event stream rather than on the subscription row.
    """

    name: str
    key: None | str | Unset = UNSET
    has_stripe_customer: bool | Unset = False
    expires_at: datetime.datetime | None | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    deleted_at: datetime.datetime | None | Unset = UNSET
    product_subscriptions: AccountProductSubscriptions | None | Unset = UNSET
    entry_point: None | str | Unset = UNSET
    show_sample_data: bool | None | Unset = UNSET
    discount_override_pct: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.account_product_subscriptions import AccountProductSubscriptions

        name = self.name

        key: None | str | Unset
        if isinstance(self.key, Unset):
            key = UNSET
        else:
            key = self.key

        has_stripe_customer = self.has_stripe_customer

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        deleted_at: None | str | Unset
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        product_subscriptions: dict[str, Any] | None | Unset
        if isinstance(self.product_subscriptions, Unset):
            product_subscriptions = UNSET
        elif isinstance(self.product_subscriptions, AccountProductSubscriptions):
            product_subscriptions = self.product_subscriptions.to_dict()
        else:
            product_subscriptions = self.product_subscriptions

        entry_point: None | str | Unset
        if isinstance(self.entry_point, Unset):
            entry_point = UNSET
        else:
            entry_point = self.entry_point

        show_sample_data: bool | None | Unset
        if isinstance(self.show_sample_data, Unset):
            show_sample_data = UNSET
        else:
            show_sample_data = self.show_sample_data

        discount_override_pct: int | None | Unset
        if isinstance(self.discount_override_pct, Unset):
            discount_override_pct = UNSET
        else:
            discount_override_pct = self.discount_override_pct

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if key is not UNSET:
            field_dict["key"] = key
        if has_stripe_customer is not UNSET:
            field_dict["has_stripe_customer"] = has_stripe_customer
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if product_subscriptions is not UNSET:
            field_dict["product_subscriptions"] = product_subscriptions
        if entry_point is not UNSET:
            field_dict["entry_point"] = entry_point
        if show_sample_data is not UNSET:
            field_dict["show_sample_data"] = show_sample_data
        if discount_override_pct is not UNSET:
            field_dict["discount_override_pct"] = discount_override_pct

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_product_subscriptions import AccountProductSubscriptions

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        key = _parse_key(d.pop("key", UNSET))

        has_stripe_customer = d.pop("has_stripe_customer", UNSET)

        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

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

        def _parse_deleted_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_at_type_0 = isoparse(data)

                return deleted_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at", UNSET))

        def _parse_product_subscriptions(data: object) -> AccountProductSubscriptions | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                product_subscriptions_type_0 = AccountProductSubscriptions.from_dict(data)

                return product_subscriptions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AccountProductSubscriptions | None | Unset, data)

        product_subscriptions = _parse_product_subscriptions(d.pop("product_subscriptions", UNSET))

        def _parse_entry_point(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        entry_point = _parse_entry_point(d.pop("entry_point", UNSET))

        def _parse_show_sample_data(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        show_sample_data = _parse_show_sample_data(d.pop("show_sample_data", UNSET))

        def _parse_discount_override_pct(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        discount_override_pct = _parse_discount_override_pct(d.pop("discount_override_pct", UNSET))

        account = cls(
            name=name,
            key=key,
            has_stripe_customer=has_stripe_customer,
            expires_at=expires_at,
            created_at=created_at,
            deleted_at=deleted_at,
            product_subscriptions=product_subscriptions,
            entry_point=entry_point,
            show_sample_data=show_sample_data,
            discount_override_pct=discount_override_pct,
        )

        account.additional_properties = d
        return account

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
