from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)
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
        run (Union['RunResponse', None, Unset]): Full run details when a run was created. None in dry_run mode or when
            skipped.
        run_id (Union[None, UUID, Unset]): The ID of the created run. None in dry_run mode or when skipped.
        status (Union[Unset, TriggeredJobStatus]): Why the job did or did not start. 'skipped_fresh' — freshness already
            satisfied or an upstream is not completed. 'skipped_upstream_pending' — upstream being re-run in same batch.
            'skipped_out_of_interval' — point-in-time trigger outside script.interval_start/end. 'skipped_concurrency_limit'
            — active run count already at the script's concurrency limit. 'skipped_already_covered' — scheduler/cascade
            detected prior completed run already covers the period. Default: TriggeredJobStatus.TRIGGERED.
    """

    job_ref: str
    matched_triggers: list[str]
    script_id: UUID
    trigger: str
    run: Union["RunResponse", None, Unset] = UNSET
    run_id: Union[None, UUID, Unset] = UNSET
    status: Union[Unset, TriggeredJobStatus] = TriggeredJobStatus.TRIGGERED
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.run_response import RunResponse

        job_ref = self.job_ref

        matched_triggers = self.matched_triggers

        script_id = str(self.script_id)

        trigger = self.trigger

        run: Union[None, Unset, dict[str, Any]]
        if isinstance(self.run, Unset):
            run = UNSET
        elif isinstance(self.run, RunResponse):
            run = self.run.to_dict()
        else:
            run = self.run

        run_id: Union[None, Unset, str]
        if isinstance(self.run_id, Unset):
            run_id = UNSET
        elif isinstance(self.run_id, UUID):
            run_id = str(self.run_id)
        else:
            run_id = self.run_id

        status: Union[Unset, str] = UNSET
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

        def _parse_run(data: object) -> Union["RunResponse", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                run_type_0 = RunResponse.from_dict(data)

                return run_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunResponse", None, Unset], data)

        run = _parse_run(d.pop("run", UNSET))

        def _parse_run_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                run_id_type_0 = UUID(data)

                return run_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        run_id = _parse_run_id(d.pop("run_id", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, TriggeredJobStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = TriggeredJobStatus(_status)

        triggered_job = cls(
            job_ref=job_ref,
            matched_triggers=matched_triggers,
            script_id=script_id,
            trigger=trigger,
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
