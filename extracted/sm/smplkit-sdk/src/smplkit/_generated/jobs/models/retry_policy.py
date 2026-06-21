from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.retry_policy_backoff import check_retry_policy_backoff
from ..models.retry_policy_backoff import RetryPolicyBackoff
from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.retry_on import RetryOn


T = TypeVar("T", bound="RetryPolicy")


@_attrs_define
class RetryPolicy:
    """A named, reusable automatic-retry policy.

    A policy decides whether and how a failed run is retried. Reference it from
    a job's `retry_policy` (and optionally override it per environment). A job
    that references nothing uses the built-in `Default` policy, which never
    retries.

        Attributes:
            name (str): Human-readable name for the policy.
            max_retries (int): How many times a failed run is retried, after the initial attempt — so `max_retries` of 3
                means up to 4 attempts in total. `0` disables retries. Maximum 10.
            backoff (RetryPolicyBackoff): How the wait between retries grows. `fixed` waits `delay_seconds` before every
                retry. `exponential` doubles the wait each time — `delay_seconds`, then `2×`, `4×`, … — capped at
                `max_delay_seconds`.
            delay_seconds (int): The wait before a retry, in seconds. For `fixed` backoff it is the constant wait before
                every retry; for `exponential` it is the base wait that doubles each retry.
            max_delay_seconds (int | None | Unset): The ceiling on the wait between retries, in seconds, for `exponential`
                backoff — once the doubling reaches it, every subsequent retry waits this long. Only valid with `exponential`
                backoff; omit it for `fixed`.
            retry_on (RetryOn | Unset): Which failures a policy retries. An empty policy (both lists empty or
                absent) retries nothing.
            created_at (datetime.datetime | None | Unset): When the policy was created.
            updated_at (datetime.datetime | None | Unset): When the policy was last modified.
            deleted_at (datetime.datetime | None | Unset): When the policy was deleted. `null` for active policies.
            version (int | None | Unset): Monotonic counter incremented on every update, starting at 1.
    """

    name: str
    max_retries: int
    backoff: RetryPolicyBackoff
    delay_seconds: int
    max_delay_seconds: int | None | Unset = UNSET
    retry_on: RetryOn | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    deleted_at: datetime.datetime | None | Unset = UNSET
    version: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        max_retries = self.max_retries

        backoff: str = self.backoff

        delay_seconds = self.delay_seconds

        max_delay_seconds: int | None | Unset
        if isinstance(self.max_delay_seconds, Unset):
            max_delay_seconds = UNSET
        else:
            max_delay_seconds = self.max_delay_seconds

        retry_on: dict[str, Any] | Unset = UNSET
        if not isinstance(self.retry_on, Unset):
            retry_on = self.retry_on.to_dict()

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

        deleted_at: None | str | Unset
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        version: int | None | Unset
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "max_retries": max_retries,
                "backoff": backoff,
                "delay_seconds": delay_seconds,
            }
        )
        if max_delay_seconds is not UNSET:
            field_dict["max_delay_seconds"] = max_delay_seconds
        if retry_on is not UNSET:
            field_dict["retry_on"] = retry_on
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.retry_on import RetryOn

        d = dict(src_dict)
        name = d.pop("name")

        max_retries = d.pop("max_retries")

        backoff = check_retry_policy_backoff(d.pop("backoff"))

        delay_seconds = d.pop("delay_seconds")

        def _parse_max_delay_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_delay_seconds = _parse_max_delay_seconds(d.pop("max_delay_seconds", UNSET))

        _retry_on = d.pop("retry_on", UNSET)
        retry_on: RetryOn | Unset
        if isinstance(_retry_on, Unset):
            retry_on = UNSET
        else:
            retry_on = RetryOn.from_dict(_retry_on)

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

        def _parse_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        version = _parse_version(d.pop("version", UNSET))

        retry_policy = cls(
            name=name,
            max_retries=max_retries,
            backoff=backoff,
            delay_seconds=delay_seconds,
            max_delay_seconds=max_delay_seconds,
            retry_on=retry_on,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            version=version,
        )

        retry_policy.additional_properties = d
        return retry_policy

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
