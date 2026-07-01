from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.organization_plan_type import OrganizationPlanType
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationPlanResponse")


@_attrs_define
class OrganizationPlanResponse:
    """
    Attributes:
        date_added (datetime.datetime): datetime with the constraint that the value must have timezone info
        date_updated (datetime.datetime): datetime with the constraint that the value must have timezone info
        id (UUID): The unique ID of the entity
        plan (OrganizationPlanType): The plan type (trial, paid)
        max_concurrent_runs (int | None | Unset): Concurrent-run cap; null when unlimited.
        max_run_seconds (int | None | Unset): Per-run duration cap in seconds; null when unlimited.
        seconds_limit (int | None | Unset): Monthly run-seconds budget; null when unlimited.
        trial_days_remaining (int | None | Unset): Days remaining in trial. Positive when active, zero or negative when
            expired. Null for non-trial plans.
        trial_expires_at (datetime.datetime | None | Unset): When the trial expires; null for non-trial plans.
        trial_started_at (datetime.datetime | None | Unset): When the trial started; null for non-trial plans.
    """

    date_added: datetime.datetime
    date_updated: datetime.datetime
    id: UUID
    plan: OrganizationPlanType
    max_concurrent_runs: int | None | Unset = UNSET
    max_run_seconds: int | None | Unset = UNSET
    seconds_limit: int | None | Unset = UNSET
    trial_days_remaining: int | None | Unset = UNSET
    trial_expires_at: datetime.datetime | None | Unset = UNSET
    trial_started_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        id = str(self.id)

        plan = self.plan.value

        max_concurrent_runs: int | None | Unset
        if isinstance(self.max_concurrent_runs, Unset):
            max_concurrent_runs = UNSET
        else:
            max_concurrent_runs = self.max_concurrent_runs

        max_run_seconds: int | None | Unset
        if isinstance(self.max_run_seconds, Unset):
            max_run_seconds = UNSET
        else:
            max_run_seconds = self.max_run_seconds

        seconds_limit: int | None | Unset
        if isinstance(self.seconds_limit, Unset):
            seconds_limit = UNSET
        else:
            seconds_limit = self.seconds_limit

        trial_days_remaining: int | None | Unset
        if isinstance(self.trial_days_remaining, Unset):
            trial_days_remaining = UNSET
        else:
            trial_days_remaining = self.trial_days_remaining

        trial_expires_at: None | str | Unset
        if isinstance(self.trial_expires_at, Unset):
            trial_expires_at = UNSET
        elif isinstance(self.trial_expires_at, datetime.datetime):
            trial_expires_at = self.trial_expires_at.isoformat()
        else:
            trial_expires_at = self.trial_expires_at

        trial_started_at: None | str | Unset
        if isinstance(self.trial_started_at, Unset):
            trial_started_at = UNSET
        elif isinstance(self.trial_started_at, datetime.datetime):
            trial_started_at = self.trial_started_at.isoformat()
        else:
            trial_started_at = self.trial_started_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date_added": date_added,
                "date_updated": date_updated,
                "id": id,
                "plan": plan,
            }
        )
        if max_concurrent_runs is not UNSET:
            field_dict["max_concurrent_runs"] = max_concurrent_runs
        if max_run_seconds is not UNSET:
            field_dict["max_run_seconds"] = max_run_seconds
        if seconds_limit is not UNSET:
            field_dict["seconds_limit"] = seconds_limit
        if trial_days_remaining is not UNSET:
            field_dict["trial_days_remaining"] = trial_days_remaining
        if trial_expires_at is not UNSET:
            field_dict["trial_expires_at"] = trial_expires_at
        if trial_started_at is not UNSET:
            field_dict["trial_started_at"] = trial_started_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        id = UUID(d.pop("id"))

        plan = OrganizationPlanType(d.pop("plan"))

        def _parse_max_concurrent_runs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_concurrent_runs = _parse_max_concurrent_runs(
            d.pop("max_concurrent_runs", UNSET)
        )

        def _parse_max_run_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_run_seconds = _parse_max_run_seconds(d.pop("max_run_seconds", UNSET))

        def _parse_seconds_limit(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        seconds_limit = _parse_seconds_limit(d.pop("seconds_limit", UNSET))

        def _parse_trial_days_remaining(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        trial_days_remaining = _parse_trial_days_remaining(
            d.pop("trial_days_remaining", UNSET)
        )

        def _parse_trial_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                trial_expires_at_type_0 = isoparse(data)

                return trial_expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        trial_expires_at = _parse_trial_expires_at(d.pop("trial_expires_at", UNSET))

        def _parse_trial_started_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                trial_started_at_type_0 = isoparse(data)

                return trial_started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        trial_started_at = _parse_trial_started_at(d.pop("trial_started_at", UNSET))

        organization_plan_response = cls(
            date_added=date_added,
            date_updated=date_updated,
            id=id,
            plan=plan,
            max_concurrent_runs=max_concurrent_runs,
            max_run_seconds=max_run_seconds,
            seconds_limit=seconds_limit,
            trial_days_remaining=trial_days_remaining,
            trial_expires_at=trial_expires_at,
            trial_started_at=trial_started_at,
        )

        organization_plan_response.additional_properties = d
        return organization_plan_response

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
