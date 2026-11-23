from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.access_state import AccessState

if TYPE_CHECKING:
    from ..models.fresh_provider_value import FreshProviderValue
    from ..models.stale_provider_value import StaleProviderValue
    from ..models.unavailable_provider_value import UnavailableProviderValue


T = TypeVar("T", bound="BillingAccount")


@_attrs_define
class BillingAccount:
    """
    Attributes:
        tenant_id (str):
        access_state (AccessState): Current billing access state.
        currency (str):
        credit_balance (FreshProviderValue | StaleProviderValue | UnavailableProviderValue): Provider-backed amount with
            typed freshness semantics.
        payment_method_status (None | str):
        revision (int):
        max_runtimes (int | None):
        max_vcpus (int | None):
        max_memory_mib (int | None):
        max_image_builds_active (int | None):
        max_image_builds_queued (int | None):
        max_image_build_minutes_daily (int | None):
        max_image_build_retries (int | None):
        restriction_reason (None | str):
        payment_grace_expires_at (datetime.datetime | None):
    """

    tenant_id: str
    access_state: AccessState
    currency: str
    credit_balance: FreshProviderValue | StaleProviderValue | UnavailableProviderValue
    payment_method_status: None | str
    revision: int
    max_runtimes: int | None
    max_vcpus: int | None
    max_memory_mib: int | None
    max_image_builds_active: int | None
    max_image_builds_queued: int | None
    max_image_build_minutes_daily: int | None
    max_image_build_retries: int | None
    restriction_reason: None | str
    payment_grace_expires_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.fresh_provider_value import FreshProviderValue
        from ..models.stale_provider_value import StaleProviderValue

        tenant_id = self.tenant_id

        access_state = self.access_state.value

        currency = self.currency

        credit_balance: dict[str, Any]
        if isinstance(self.credit_balance, FreshProviderValue):
            credit_balance = self.credit_balance.to_dict()
        elif isinstance(self.credit_balance, StaleProviderValue):
            credit_balance = self.credit_balance.to_dict()
        else:
            credit_balance = self.credit_balance.to_dict()

        payment_method_status: None | str
        payment_method_status = self.payment_method_status

        revision = self.revision

        max_runtimes: int | None
        max_runtimes = self.max_runtimes

        max_vcpus: int | None
        max_vcpus = self.max_vcpus

        max_memory_mib: int | None
        max_memory_mib = self.max_memory_mib

        max_image_builds_active: int | None
        max_image_builds_active = self.max_image_builds_active

        max_image_builds_queued: int | None
        max_image_builds_queued = self.max_image_builds_queued

        max_image_build_minutes_daily: int | None
        max_image_build_minutes_daily = self.max_image_build_minutes_daily

        max_image_build_retries: int | None
        max_image_build_retries = self.max_image_build_retries

        restriction_reason: None | str
        restriction_reason = self.restriction_reason

        payment_grace_expires_at: None | str
        if isinstance(self.payment_grace_expires_at, datetime.datetime):
            payment_grace_expires_at = self.payment_grace_expires_at.isoformat()
        else:
            payment_grace_expires_at = self.payment_grace_expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tenant_id": tenant_id,
                "access_state": access_state,
                "currency": currency,
                "credit_balance": credit_balance,
                "payment_method_status": payment_method_status,
                "revision": revision,
                "max_runtimes": max_runtimes,
                "max_vcpus": max_vcpus,
                "max_memory_mib": max_memory_mib,
                "max_image_builds_active": max_image_builds_active,
                "max_image_builds_queued": max_image_builds_queued,
                "max_image_build_minutes_daily": max_image_build_minutes_daily,
                "max_image_build_retries": max_image_build_retries,
                "restriction_reason": restriction_reason,
                "payment_grace_expires_at": payment_grace_expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fresh_provider_value import FreshProviderValue
        from ..models.stale_provider_value import StaleProviderValue
        from ..models.unavailable_provider_value import UnavailableProviderValue

        d = dict(src_dict)
        tenant_id = d.pop("tenant_id")

        access_state = AccessState(d.pop("access_state"))

        currency = d.pop("currency")

        def _parse_credit_balance(
            data: object,
        ) -> FreshProviderValue | StaleProviderValue | UnavailableProviderValue:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_provider_value_type_0 = FreshProviderValue.from_dict(
                    data
                )

                return componentsschemas_provider_value_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_provider_value_type_1 = StaleProviderValue.from_dict(
                    data
                )

                return componentsschemas_provider_value_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_provider_value_type_2 = (
                UnavailableProviderValue.from_dict(data)
            )

            return componentsschemas_provider_value_type_2

        credit_balance = _parse_credit_balance(d.pop("credit_balance"))

        def _parse_payment_method_status(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        payment_method_status = _parse_payment_method_status(
            d.pop("payment_method_status")
        )

        revision = d.pop("revision")

        def _parse_max_runtimes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_runtimes = _parse_max_runtimes(d.pop("max_runtimes"))

        def _parse_max_vcpus(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_vcpus = _parse_max_vcpus(d.pop("max_vcpus"))

        def _parse_max_memory_mib(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_memory_mib = _parse_max_memory_mib(d.pop("max_memory_mib"))

        def _parse_max_image_builds_active(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_image_builds_active = _parse_max_image_builds_active(
            d.pop("max_image_builds_active")
        )

        def _parse_max_image_builds_queued(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_image_builds_queued = _parse_max_image_builds_queued(
            d.pop("max_image_builds_queued")
        )

        def _parse_max_image_build_minutes_daily(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_image_build_minutes_daily = _parse_max_image_build_minutes_daily(
            d.pop("max_image_build_minutes_daily")
        )

        def _parse_max_image_build_retries(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_image_build_retries = _parse_max_image_build_retries(
            d.pop("max_image_build_retries")
        )

        def _parse_restriction_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        restriction_reason = _parse_restriction_reason(d.pop("restriction_reason"))

        def _parse_payment_grace_expires_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                payment_grace_expires_at_type_0 = datetime.datetime.fromisoformat(
                    data.replace("Z", "+00:00")
                )

                return payment_grace_expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        payment_grace_expires_at = _parse_payment_grace_expires_at(
            d.pop("payment_grace_expires_at")
        )

        billing_account = cls(
            tenant_id=tenant_id,
            access_state=access_state,
            currency=currency,
            credit_balance=credit_balance,
            payment_method_status=payment_method_status,
            revision=revision,
            max_runtimes=max_runtimes,
            max_vcpus=max_vcpus,
            max_memory_mib=max_memory_mib,
            max_image_builds_active=max_image_builds_active,
            max_image_builds_queued=max_image_builds_queued,
            max_image_build_minutes_daily=max_image_build_minutes_daily,
            max_image_build_retries=max_image_build_retries,
            restriction_reason=restriction_reason,
            payment_grace_expires_at=payment_grace_expires_at,
        )

        billing_account.additional_properties = d
        return billing_account

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
