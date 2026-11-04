from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.run_mode import RunMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateJobRunRequest")


@_attrs_define
class CreateJobRunRequest:
    """
    Attributes:
        job_id (UUID): The ID of the job to run.
        trigger (str): The trigger recorded on the run, e.g. `manual:jobs.my_job`, `schedule:0 8 * * *`. Must be a valid
            trigger string.
        mode (RunMode | Unset): How to create a run: `always` creates a new run; `when_not_running` returns the job's
            pending, starting or running run if it has one, otherwise creates a new one.
        profile (None | str | Unset): The profile to run under; defaults to the job's own profile.
        refresh (bool | Unset): Start the run as a refresh: the job's progress goes back to its interval start and the
            run receives `refresh: true` in its run context, leaving what to reload to the job's code. The progress of the
            jobs downstream of it is reset too. Ignored when the job's `refresh_propagation` is `block`. Default: False.
        skip_freshness (bool | Unset): Start the run even if its upstream jobs are not fresh. When false and an upstream
            is stale, no run is created and the call answers 409 `upstream_not_fresh`. Default: False.
    """

    job_id: UUID
    trigger: str
    mode: RunMode | Unset = UNSET
    profile: None | str | Unset = UNSET
    refresh: bool | Unset = False
    skip_freshness: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = str(self.job_id)

        trigger = self.trigger

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        profile: None | str | Unset
        if isinstance(self.profile, Unset):
            profile = UNSET
        else:
            profile = self.profile

        refresh = self.refresh

        skip_freshness = self.skip_freshness

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
                "trigger": trigger,
            }
        )
        if mode is not UNSET:
            field_dict["mode"] = mode
        if profile is not UNSET:
            field_dict["profile"] = profile
        if refresh is not UNSET:
            field_dict["refresh"] = refresh
        if skip_freshness is not UNSET:
            field_dict["skip_freshness"] = skip_freshness

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_id = UUID(d.pop("job_id"))

        trigger = d.pop("trigger")

        _mode = d.pop("mode", UNSET)
        mode: RunMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = RunMode(_mode)

        def _parse_profile(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        profile = _parse_profile(d.pop("profile", UNSET))

        refresh = d.pop("refresh", UNSET)

        skip_freshness = d.pop("skip_freshness", UNSET)

        create_job_run_request = cls(
            job_id=job_id,
            trigger=trigger,
            mode=mode,
            profile=profile,
            refresh=refresh,
            skip_freshness=skip_freshness,
        )

        create_job_run_request.additional_properties = d
        return create_job_run_request

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
