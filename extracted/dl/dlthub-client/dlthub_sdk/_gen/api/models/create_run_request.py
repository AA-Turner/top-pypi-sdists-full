from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.run_mode import RunMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateRunRequest")


@_attrs_define
class CreateRunRequest:
    """
    Attributes:
        script_id_or_ref (str): The ID or job_ref of the script to run.
        trigger (str): The trigger that starts this run, must be one of the triggers defined in the job definition (e.g.
            manual:, schedule:0 8 * * *, tag:backfill).
        mode (RunMode | Unset): Run creation mode. 'always' creates a new run every time. 'when_not_running' returns an
            existing active run if one exists, otherwise creates a new one.
        profile (None | str | Unset): The name of the profile to use for the run, will default to the default profile of
            the script.
        refresh (bool | Unset): When true, eagerly clear the script's prev_completed_run and all transitive freshness-
            graph downstream, then ship a refresh signal to the launcher so the job performs a full reload instead of
            processing the interval window. Default: False.
        skip_freshness (bool | Unset): When true, bypass freshness gating and start the run even if upstream freshness
            constraints are unmet. Default false: the run is skipped (status='skipped_fresh') when upstreams are not fresh.
            Use this opt-in only when the caller explicitly wants to run regardless of upstream state. Default: False.
    """

    script_id_or_ref: str
    trigger: str
    mode: RunMode | Unset = UNSET
    profile: None | str | Unset = UNSET
    refresh: bool | Unset = False
    skip_freshness: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        script_id_or_ref = self.script_id_or_ref

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
                "script_id_or_ref": script_id_or_ref,
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
        script_id_or_ref = d.pop("script_id_or_ref")

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

        create_run_request = cls(
            script_id_or_ref=script_id_or_ref,
            trigger=trigger,
            mode=mode,
            profile=profile,
            refresh=refresh,
            skip_freshness=skip_freshness,
        )

        create_run_request.additional_properties = d
        return create_run_request

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
