import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.exportable_completed_job_job_kind import ExportableCompletedJobJobKind
from ..models.exportable_completed_job_language import ExportableCompletedJobLanguage
from ..models.exportable_completed_job_trigger_kind import ExportableCompletedJobTriggerKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.exportable_completed_job_args import ExportableCompletedJobArgs
    from ..models.exportable_completed_job_flow_status import ExportableCompletedJobFlowStatus
    from ..models.exportable_completed_job_raw_flow import ExportableCompletedJobRawFlow
    from ..models.exportable_completed_job_result import ExportableCompletedJobResult
    from ..models.exportable_completed_job_workflow_as_code_status import ExportableCompletedJobWorkflowAsCodeStatus


T = TypeVar("T", bound="ExportableCompletedJob")


@_attrs_define
class ExportableCompletedJob:
    """Completed job with full data for export/import operations

    Attributes:
        id (str):
        created_by (str):
        created_at (datetime.datetime):
        job_kind (ExportableCompletedJobJobKind):
        permissioned_as (str):
        email (str):
        visible_to_owner (bool):
        parent_job (Union[Unset, str]):
        started_at (Union[Unset, datetime.datetime]):
        completed_at (Union[Unset, datetime.datetime]):
        duration_ms (Union[Unset, int]):
        script_path (Union[Unset, str]):
        script_hash (Union[Unset, str]):
        args (Union[Unset, ExportableCompletedJobArgs]): Full job arguments without size restrictions
        result (Union[Unset, ExportableCompletedJobResult]): Full job result without size restrictions
        logs (Union[Unset, str]): Complete job logs from v2_job table
        raw_code (Union[Unset, str]):
        raw_lock (Union[Unset, str]):
        canceled_by (Union[Unset, str]):
        canceled_reason (Union[Unset, str]):
        trigger (Union[Unset, str]): Trigger path for the job (replaces schedule_path)
        trigger_kind (Union[Unset, ExportableCompletedJobTriggerKind]):
        permissioned_as_email (Union[Unset, str]):
        flow_status (Union[Unset, ExportableCompletedJobFlowStatus]): Flow status from v2_job_status table
        workflow_as_code_status (Union[Unset, ExportableCompletedJobWorkflowAsCodeStatus]):
        raw_flow (Union[Unset, ExportableCompletedJobRawFlow]):
        is_flow_step (Union[Unset, bool]):
        language (Union[Unset, ExportableCompletedJobLanguage]):
        is_skipped (Union[Unset, bool]):
        mem_peak (Union[Unset, int]):
        tag (Union[Unset, str]):
        priority (Union[Unset, int]):
        labels (Union[Unset, List[str]]):
        same_worker (Union[Unset, bool]):
        flow_step_id (Union[Unset, str]):
        flow_innermost_root_job (Union[Unset, str]):
        concurrent_limit (Union[Unset, int]):
        concurrency_time_window_s (Union[Unset, int]):
        timeout (Union[Unset, int]):
        cache_ttl (Union[Unset, int]):
        self_wait_time_ms (Union[Unset, int]):
        aggregate_wait_time_ms (Union[Unset, int]):
        preprocessed (Union[Unset, bool]):
        worker (Union[Unset, str]):
        status (Union[Unset, str]): Actual job status from database
    """

    id: str
    created_by: str
    created_at: datetime.datetime
    job_kind: ExportableCompletedJobJobKind
    permissioned_as: str
    email: str
    visible_to_owner: bool
    parent_job: Union[Unset, str] = UNSET
    started_at: Union[Unset, datetime.datetime] = UNSET
    completed_at: Union[Unset, datetime.datetime] = UNSET
    duration_ms: Union[Unset, int] = UNSET
    script_path: Union[Unset, str] = UNSET
    script_hash: Union[Unset, str] = UNSET
    args: Union[Unset, "ExportableCompletedJobArgs"] = UNSET
    result: Union[Unset, "ExportableCompletedJobResult"] = UNSET
    logs: Union[Unset, str] = UNSET
    raw_code: Union[Unset, str] = UNSET
    raw_lock: Union[Unset, str] = UNSET
    canceled_by: Union[Unset, str] = UNSET
    canceled_reason: Union[Unset, str] = UNSET
    trigger: Union[Unset, str] = UNSET
    trigger_kind: Union[Unset, ExportableCompletedJobTriggerKind] = UNSET
    permissioned_as_email: Union[Unset, str] = UNSET
    flow_status: Union[Unset, "ExportableCompletedJobFlowStatus"] = UNSET
    workflow_as_code_status: Union[Unset, "ExportableCompletedJobWorkflowAsCodeStatus"] = UNSET
    raw_flow: Union[Unset, "ExportableCompletedJobRawFlow"] = UNSET
    is_flow_step: Union[Unset, bool] = UNSET
    language: Union[Unset, ExportableCompletedJobLanguage] = UNSET
    is_skipped: Union[Unset, bool] = UNSET
    mem_peak: Union[Unset, int] = UNSET
    tag: Union[Unset, str] = UNSET
    priority: Union[Unset, int] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    same_worker: Union[Unset, bool] = UNSET
    flow_step_id: Union[Unset, str] = UNSET
    flow_innermost_root_job: Union[Unset, str] = UNSET
    concurrent_limit: Union[Unset, int] = UNSET
    concurrency_time_window_s: Union[Unset, int] = UNSET
    timeout: Union[Unset, int] = UNSET
    cache_ttl: Union[Unset, int] = UNSET
    self_wait_time_ms: Union[Unset, int] = UNSET
    aggregate_wait_time_ms: Union[Unset, int] = UNSET
    preprocessed: Union[Unset, bool] = UNSET
    worker: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_by = self.created_by
        created_at = self.created_at.isoformat()

        job_kind = self.job_kind.value

        permissioned_as = self.permissioned_as
        email = self.email
        visible_to_owner = self.visible_to_owner
        parent_job = self.parent_job
        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        completed_at: Union[Unset, str] = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        duration_ms = self.duration_ms
        script_path = self.script_path
        script_hash = self.script_hash
        args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args.to_dict()

        result: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

        logs = self.logs
        raw_code = self.raw_code
        raw_lock = self.raw_lock
        canceled_by = self.canceled_by
        canceled_reason = self.canceled_reason
        trigger = self.trigger
        trigger_kind: Union[Unset, str] = UNSET
        if not isinstance(self.trigger_kind, Unset):
            trigger_kind = self.trigger_kind.value

        permissioned_as_email = self.permissioned_as_email
        flow_status: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow_status, Unset):
            flow_status = self.flow_status.to_dict()

        workflow_as_code_status: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.workflow_as_code_status, Unset):
            workflow_as_code_status = self.workflow_as_code_status.to_dict()

        raw_flow: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.raw_flow, Unset):
            raw_flow = self.raw_flow.to_dict()

        is_flow_step = self.is_flow_step
        language: Union[Unset, str] = UNSET
        if not isinstance(self.language, Unset):
            language = self.language.value

        is_skipped = self.is_skipped
        mem_peak = self.mem_peak
        tag = self.tag
        priority = self.priority
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        same_worker = self.same_worker
        flow_step_id = self.flow_step_id
        flow_innermost_root_job = self.flow_innermost_root_job
        concurrent_limit = self.concurrent_limit
        concurrency_time_window_s = self.concurrency_time_window_s
        timeout = self.timeout
        cache_ttl = self.cache_ttl
        self_wait_time_ms = self.self_wait_time_ms
        aggregate_wait_time_ms = self.aggregate_wait_time_ms
        preprocessed = self.preprocessed
        worker = self.worker
        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_by": created_by,
                "created_at": created_at,
                "job_kind": job_kind,
                "permissioned_as": permissioned_as,
                "email": email,
                "visible_to_owner": visible_to_owner,
            }
        )
        if parent_job is not UNSET:
            field_dict["parent_job"] = parent_job
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms
        if script_path is not UNSET:
            field_dict["script_path"] = script_path
        if script_hash is not UNSET:
            field_dict["script_hash"] = script_hash
        if args is not UNSET:
            field_dict["args"] = args
        if result is not UNSET:
            field_dict["result"] = result
        if logs is not UNSET:
            field_dict["logs"] = logs
        if raw_code is not UNSET:
            field_dict["raw_code"] = raw_code
        if raw_lock is not UNSET:
            field_dict["raw_lock"] = raw_lock
        if canceled_by is not UNSET:
            field_dict["canceled_by"] = canceled_by
        if canceled_reason is not UNSET:
            field_dict["canceled_reason"] = canceled_reason
        if trigger is not UNSET:
            field_dict["trigger"] = trigger
        if trigger_kind is not UNSET:
            field_dict["trigger_kind"] = trigger_kind
        if permissioned_as_email is not UNSET:
            field_dict["permissioned_as_email"] = permissioned_as_email
        if flow_status is not UNSET:
            field_dict["flow_status"] = flow_status
        if workflow_as_code_status is not UNSET:
            field_dict["workflow_as_code_status"] = workflow_as_code_status
        if raw_flow is not UNSET:
            field_dict["raw_flow"] = raw_flow
        if is_flow_step is not UNSET:
            field_dict["is_flow_step"] = is_flow_step
        if language is not UNSET:
            field_dict["language"] = language
        if is_skipped is not UNSET:
            field_dict["is_skipped"] = is_skipped
        if mem_peak is not UNSET:
            field_dict["mem_peak"] = mem_peak
        if tag is not UNSET:
            field_dict["tag"] = tag
        if priority is not UNSET:
            field_dict["priority"] = priority
        if labels is not UNSET:
            field_dict["labels"] = labels
        if same_worker is not UNSET:
            field_dict["same_worker"] = same_worker
        if flow_step_id is not UNSET:
            field_dict["flow_step_id"] = flow_step_id
        if flow_innermost_root_job is not UNSET:
            field_dict["flow_innermost_root_job"] = flow_innermost_root_job
        if concurrent_limit is not UNSET:
            field_dict["concurrent_limit"] = concurrent_limit
        if concurrency_time_window_s is not UNSET:
            field_dict["concurrency_time_window_s"] = concurrency_time_window_s
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if cache_ttl is not UNSET:
            field_dict["cache_ttl"] = cache_ttl
        if self_wait_time_ms is not UNSET:
            field_dict["self_wait_time_ms"] = self_wait_time_ms
        if aggregate_wait_time_ms is not UNSET:
            field_dict["aggregate_wait_time_ms"] = aggregate_wait_time_ms
        if preprocessed is not UNSET:
            field_dict["preprocessed"] = preprocessed
        if worker is not UNSET:
            field_dict["worker"] = worker
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.exportable_completed_job_args import ExportableCompletedJobArgs
        from ..models.exportable_completed_job_flow_status import ExportableCompletedJobFlowStatus
        from ..models.exportable_completed_job_raw_flow import ExportableCompletedJobRawFlow
        from ..models.exportable_completed_job_result import ExportableCompletedJobResult
        from ..models.exportable_completed_job_workflow_as_code_status import ExportableCompletedJobWorkflowAsCodeStatus

        d = src_dict.copy()
        id = d.pop("id")

        created_by = d.pop("created_by")

        created_at = isoparse(d.pop("created_at"))

        job_kind = ExportableCompletedJobJobKind(d.pop("job_kind"))

        permissioned_as = d.pop("permissioned_as")

        email = d.pop("email")

        visible_to_owner = d.pop("visible_to_owner")

        parent_job = d.pop("parent_job", UNSET)

        _started_at = d.pop("started_at", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: Union[Unset, datetime.datetime]
        if isinstance(_completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = isoparse(_completed_at)

        duration_ms = d.pop("duration_ms", UNSET)

        script_path = d.pop("script_path", UNSET)

        script_hash = d.pop("script_hash", UNSET)

        _args = d.pop("args", UNSET)
        args: Union[Unset, ExportableCompletedJobArgs]
        if isinstance(_args, Unset):
            args = UNSET
        else:
            args = ExportableCompletedJobArgs.from_dict(_args)

        _result = d.pop("result", UNSET)
        result: Union[Unset, ExportableCompletedJobResult]
        if isinstance(_result, Unset):
            result = UNSET
        else:
            result = ExportableCompletedJobResult.from_dict(_result)

        logs = d.pop("logs", UNSET)

        raw_code = d.pop("raw_code", UNSET)

        raw_lock = d.pop("raw_lock", UNSET)

        canceled_by = d.pop("canceled_by", UNSET)

        canceled_reason = d.pop("canceled_reason", UNSET)

        trigger = d.pop("trigger", UNSET)

        _trigger_kind = d.pop("trigger_kind", UNSET)
        trigger_kind: Union[Unset, ExportableCompletedJobTriggerKind]
        if isinstance(_trigger_kind, Unset):
            trigger_kind = UNSET
        else:
            trigger_kind = ExportableCompletedJobTriggerKind(_trigger_kind)

        permissioned_as_email = d.pop("permissioned_as_email", UNSET)

        _flow_status = d.pop("flow_status", UNSET)
        flow_status: Union[Unset, ExportableCompletedJobFlowStatus]
        if isinstance(_flow_status, Unset):
            flow_status = UNSET
        else:
            flow_status = ExportableCompletedJobFlowStatus.from_dict(_flow_status)

        _workflow_as_code_status = d.pop("workflow_as_code_status", UNSET)
        workflow_as_code_status: Union[Unset, ExportableCompletedJobWorkflowAsCodeStatus]
        if isinstance(_workflow_as_code_status, Unset):
            workflow_as_code_status = UNSET
        else:
            workflow_as_code_status = ExportableCompletedJobWorkflowAsCodeStatus.from_dict(_workflow_as_code_status)

        _raw_flow = d.pop("raw_flow", UNSET)
        raw_flow: Union[Unset, ExportableCompletedJobRawFlow]
        if isinstance(_raw_flow, Unset):
            raw_flow = UNSET
        else:
            raw_flow = ExportableCompletedJobRawFlow.from_dict(_raw_flow)

        is_flow_step = d.pop("is_flow_step", UNSET)

        _language = d.pop("language", UNSET)
        language: Union[Unset, ExportableCompletedJobLanguage]
        if isinstance(_language, Unset):
            language = UNSET
        else:
            language = ExportableCompletedJobLanguage(_language)

        is_skipped = d.pop("is_skipped", UNSET)

        mem_peak = d.pop("mem_peak", UNSET)

        tag = d.pop("tag", UNSET)

        priority = d.pop("priority", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        same_worker = d.pop("same_worker", UNSET)

        flow_step_id = d.pop("flow_step_id", UNSET)

        flow_innermost_root_job = d.pop("flow_innermost_root_job", UNSET)

        concurrent_limit = d.pop("concurrent_limit", UNSET)

        concurrency_time_window_s = d.pop("concurrency_time_window_s", UNSET)

        timeout = d.pop("timeout", UNSET)

        cache_ttl = d.pop("cache_ttl", UNSET)

        self_wait_time_ms = d.pop("self_wait_time_ms", UNSET)

        aggregate_wait_time_ms = d.pop("aggregate_wait_time_ms", UNSET)

        preprocessed = d.pop("preprocessed", UNSET)

        worker = d.pop("worker", UNSET)

        status = d.pop("status", UNSET)

        exportable_completed_job = cls(
            id=id,
            created_by=created_by,
            created_at=created_at,
            job_kind=job_kind,
            permissioned_as=permissioned_as,
            email=email,
            visible_to_owner=visible_to_owner,
            parent_job=parent_job,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            script_path=script_path,
            script_hash=script_hash,
            args=args,
            result=result,
            logs=logs,
            raw_code=raw_code,
            raw_lock=raw_lock,
            canceled_by=canceled_by,
            canceled_reason=canceled_reason,
            trigger=trigger,
            trigger_kind=trigger_kind,
            permissioned_as_email=permissioned_as_email,
            flow_status=flow_status,
            workflow_as_code_status=workflow_as_code_status,
            raw_flow=raw_flow,
            is_flow_step=is_flow_step,
            language=language,
            is_skipped=is_skipped,
            mem_peak=mem_peak,
            tag=tag,
            priority=priority,
            labels=labels,
            same_worker=same_worker,
            flow_step_id=flow_step_id,
            flow_innermost_root_job=flow_innermost_root_job,
            concurrent_limit=concurrent_limit,
            concurrency_time_window_s=concurrency_time_window_s,
            timeout=timeout,
            cache_ttl=cache_ttl,
            self_wait_time_ms=self_wait_time_ms,
            aggregate_wait_time_ms=aggregate_wait_time_ms,
            preprocessed=preprocessed,
            worker=worker,
            status=status,
        )

        exportable_completed_job.additional_properties = d
        return exportable_completed_job

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
