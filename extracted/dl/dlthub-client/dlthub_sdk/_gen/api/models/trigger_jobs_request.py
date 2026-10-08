from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TriggerJobsRequest")


@_attrs_define
class TriggerJobsRequest:
    """
    Attributes:
        dry_run (bool | Unset): If true, return the receipt the trigger would produce without creating runs. Default:
            False.
        job_ids (list[UUID] | None | Unset): Jobs to trigger, each fired via its `default_trigger` (or `manual:<ref>`
            when it has none). At least one of `job_ids` or `selectors` must be non-empty.
        profile (None | str | Unset): Profile override for all triggered runs.
        refresh (bool | Unset): When true, every triggered job eagerly clears its prev_completed_run cascade and ships a
            refresh signal to the launcher. Skipped jobs are not refreshed. Default: False.
        selectors (list[str] | None | Unset): Trigger selectors (fnmatch patterns) matched against each job's triggers;
            a matching job fires the trigger it matched. Examples: 'tag:backfill', 'schedule:*', 'batch',
            'manual:jobs.mod.*'. At least one of `job_ids` or `selectors` must be non-empty.
    """

    dry_run: bool | Unset = False
    job_ids: list[UUID] | None | Unset = UNSET
    profile: None | str | Unset = UNSET
    refresh: bool | Unset = False
    selectors: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dry_run = self.dry_run

        job_ids: list[str] | None | Unset
        if isinstance(self.job_ids, Unset):
            job_ids = UNSET
        elif isinstance(self.job_ids, list):
            job_ids = []
            for job_ids_type_0_item_data in self.job_ids:
                job_ids_type_0_item = str(job_ids_type_0_item_data)
                job_ids.append(job_ids_type_0_item)

        else:
            job_ids = self.job_ids

        profile: None | str | Unset
        if isinstance(self.profile, Unset):
            profile = UNSET
        else:
            profile = self.profile

        refresh = self.refresh

        selectors: list[str] | None | Unset
        if isinstance(self.selectors, Unset):
            selectors = UNSET
        elif isinstance(self.selectors, list):
            selectors = self.selectors

        else:
            selectors = self.selectors

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run
        if job_ids is not UNSET:
            field_dict["job_ids"] = job_ids
        if profile is not UNSET:
            field_dict["profile"] = profile
        if refresh is not UNSET:
            field_dict["refresh"] = refresh
        if selectors is not UNSET:
            field_dict["selectors"] = selectors

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dry_run = d.pop("dry_run", UNSET)

        def _parse_job_ids(data: object) -> list[UUID] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                job_ids_type_0 = []
                _job_ids_type_0 = data
                for job_ids_type_0_item_data in _job_ids_type_0:
                    job_ids_type_0_item = UUID(job_ids_type_0_item_data)

                    job_ids_type_0.append(job_ids_type_0_item)

                return job_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UUID] | None | Unset, data)

        job_ids = _parse_job_ids(d.pop("job_ids", UNSET))

        def _parse_profile(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        profile = _parse_profile(d.pop("profile", UNSET))

        refresh = d.pop("refresh", UNSET)

        def _parse_selectors(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                selectors_type_0 = cast(list[str], data)

                return selectors_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        selectors = _parse_selectors(d.pop("selectors", UNSET))

        trigger_jobs_request = cls(
            dry_run=dry_run,
            job_ids=job_ids,
            profile=profile,
            refresh=refresh,
            selectors=selectors,
        )

        trigger_jobs_request.additional_properties = d
        return trigger_jobs_request

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
