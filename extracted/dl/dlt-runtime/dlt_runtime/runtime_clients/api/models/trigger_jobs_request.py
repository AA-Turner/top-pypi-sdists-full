from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TriggerJobsRequest")


@_attrs_define
class TriggerJobsRequest:
    """
    Attributes:
        dry_run (Union[Unset, bool]): If true, return matched jobs without creating runs. Default: False.
        job_refs (Union[None, Unset, list[str]]): Explicit job_refs to trigger. Each ref resolves to ONE script and
            fires it via the script's `default_trigger` (or `manual:<ref>` fallback). At least one of `selectors` or
            `job_refs` must be non-empty.
        profile (Union[None, Unset, str]): Profile override for all triggered runs.
        refresh (Union[Unset, bool]): When true, every triggered job (status='triggered') will eagerly clear its
            prev_completed_run cascade and ship a refresh signal to the launcher. Jobs whose freshness gating fails
            (status='skipped_fresh') are NOT refreshed. Default: False.
        selectors (Union[None, Unset, list[str]]): Trigger selectors (fnmatch patterns). Examples: 'tag:backfill',
            'schedule:*', 'batch', 'manual:jobs.mod.*'. At least one of `selectors` or `job_refs` must be non-empty.
    """

    dry_run: Union[Unset, bool] = False
    job_refs: Union[None, Unset, list[str]] = UNSET
    profile: Union[None, Unset, str] = UNSET
    refresh: Union[Unset, bool] = False
    selectors: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dry_run = self.dry_run

        job_refs: Union[None, Unset, list[str]]
        if isinstance(self.job_refs, Unset):
            job_refs = UNSET
        elif isinstance(self.job_refs, list):
            job_refs = self.job_refs

        else:
            job_refs = self.job_refs

        profile: Union[None, Unset, str]
        if isinstance(self.profile, Unset):
            profile = UNSET
        else:
            profile = self.profile

        refresh = self.refresh

        selectors: Union[None, Unset, list[str]]
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
        if job_refs is not UNSET:
            field_dict["job_refs"] = job_refs
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

        def _parse_job_refs(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                job_refs_type_0 = cast(list[str], data)

                return job_refs_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        job_refs = _parse_job_refs(d.pop("job_refs", UNSET))

        def _parse_profile(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        profile = _parse_profile(d.pop("profile", UNSET))

        refresh = d.pop("refresh", UNSET)

        def _parse_selectors(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                selectors_type_0 = cast(list[str], data)

                return selectors_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        selectors = _parse_selectors(d.pop("selectors", UNSET))

        trigger_jobs_request = cls(
            dry_run=dry_run,
            job_refs=job_refs,
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
