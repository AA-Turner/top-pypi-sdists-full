from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.triggered_job_status import TriggeredJobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_response import RunResponse


T = TypeVar("T", bound="TriggeredJob")


@_attrs_define
class TriggeredJob:
    """
    Attributes:
        job_ref (str): The job reference of the matched script.
        matched_triggers (list[str]): All triggers that matched the selectors.
        script_id (UUID): The ID of the matched script.
        trigger (str): The single trigger picked for this run.
        reasons (list[str] | None | Unset): Human-readable reasons explaining non-'triggered' statuses (e.g. which
            upstreams failed the freshness check). None when status is 'triggered' or no reasons were captured.
        run (None | RunResponse | Unset): Full run details when a run was created. None in dry_run mode or when skipped.
        run_id (None | Unset | UUID): The ID of the created run. None in dry_run mode or when skipped.
        status (TriggeredJobStatus | Unset): Why the job did or did not start. 'skipped_fresh' — one or more upstream
            freshness checks failed (see `reasons` for which upstreams). 'skipped_upstream_pending' — upstream being re-run
            in same batch. 'skipped_out_of_interval' — point-in-time trigger outside script.interval_start/end.
            'skipped_concurrency_limit' — active run count already at the script's concurrency limit.
            'skipped_already_covered' — scheduler/cascade detected prior completed run already covers the period.
            'skipped_trial_expired' — trial period has ended for this organization. 'skipped_minutes_limit' — organization
            has exceeded its cumulative runtime limit. 'skipped_org_concurrency_limit' — organization has reached its
            maximum number of concurrent runs. Default: TriggeredJobStatus.TRIGGERED.
    """

    job_ref: str
    matched_triggers: list[str]
    script_id: UUID
    trigger: str
    reasons: list[str] | None | Unset = UNSET
    run: None | RunResponse | Unset = UNSET
    run_id: None | Unset | UUID = UNSET
    status: TriggeredJobStatus | Unset = TriggeredJobStatus.TRIGGERED
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.run_response import RunResponse

        job_ref = self.job_ref

        matched_triggers = self.matched_triggers

        script_id = str(self.script_id)

        trigger = self.trigger

        reasons: list[str] | None | Unset
        if isinstance(self.reasons, Unset):
            reasons = UNSET
        elif isinstance(self.reasons, list):
            reasons = self.reasons

        else:
            reasons = self.reasons

        run: dict[str, Any] | None | Unset
        if isinstance(self.run, Unset):
            run = UNSET
        elif isinstance(self.run, RunResponse):
            run = self.run.to_dict()
        else:
            run = self.run

        run_id: None | str | Unset
        if isinstance(self.run_id, Unset):
            run_id = UNSET
        elif isinstance(self.run_id, UUID):
            run_id = str(self.run_id)
        else:
            run_id = self.run_id

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_ref": job_ref,
                "matched_triggers": matched_triggers,
                "script_id": script_id,
                "trigger": trigger,
            }
        )
        if reasons is not UNSET:
            field_dict["reasons"] = reasons
        if run is not UNSET:
            field_dict["run"] = run
        if run_id is not UNSET:
            field_dict["run_id"] = run_id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_response import RunResponse

        d = dict(src_dict)
        job_ref = d.pop("job_ref")

        matched_triggers = cast(list[str], d.pop("matched_triggers"))

        script_id = UUID(d.pop("script_id"))

        trigger = d.pop("trigger")

        def _parse_reasons(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                reasons_type_0 = cast(list[str], data)

                return reasons_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        reasons = _parse_reasons(d.pop("reasons", UNSET))

        def _parse_run(data: object) -> None | RunResponse | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                run_type_0 = RunResponse.from_dict(data)

                return run_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunResponse | Unset, data)

        run = _parse_run(d.pop("run", UNSET))

        def _parse_run_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                run_id_type_0 = UUID(data)

                return run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        run_id = _parse_run_id(d.pop("run_id", UNSET))

        _status = d.pop("status", UNSET)
        status: TriggeredJobStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = TriggeredJobStatus(_status)

        triggered_job = cls(
            job_ref=job_ref,
            matched_triggers=matched_triggers,
            script_id=script_id,
            trigger=trigger,
            reasons=reasons,
            run=run,
            run_id=run_id,
            status=status,
        )

        triggered_job.additional_properties = d
        return triggered_job

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
