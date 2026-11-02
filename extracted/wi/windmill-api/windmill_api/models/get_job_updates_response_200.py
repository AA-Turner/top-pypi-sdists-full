from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_job_updates_response_200_flow_status import GetJobUpdatesResponse200FlowStatus
    from ..models.get_job_updates_response_200_workflow_as_code_status import (
        GetJobUpdatesResponse200WorkflowAsCodeStatus,
    )


T = TypeVar("T", bound="GetJobUpdatesResponse200")


@_attrs_define
class GetJobUpdatesResponse200:
    """
    Attributes:
        running (Union[Unset, bool]):
        completed (Union[Unset, bool]):
        new_logs (Union[Unset, str]):
        log_offset (Union[Unset, int]):
        mem_peak (Union[Unset, int]):
        progress (Union[Unset, int]):
        stream_offset (Union[Unset, int]):
        new_result_stream (Union[Unset, str]):
        flow_status (Union[Unset, GetJobUpdatesResponse200FlowStatus]):
        workflow_as_code_status (Union[Unset, GetJobUpdatesResponse200WorkflowAsCodeStatus]):
    """

    running: Union[Unset, bool] = UNSET
    completed: Union[Unset, bool] = UNSET
    new_logs: Union[Unset, str] = UNSET
    log_offset: Union[Unset, int] = UNSET
    mem_peak: Union[Unset, int] = UNSET
    progress: Union[Unset, int] = UNSET
    stream_offset: Union[Unset, int] = UNSET
    new_result_stream: Union[Unset, str] = UNSET
    flow_status: Union[Unset, "GetJobUpdatesResponse200FlowStatus"] = UNSET
    workflow_as_code_status: Union[Unset, "GetJobUpdatesResponse200WorkflowAsCodeStatus"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        running = self.running
        completed = self.completed
        new_logs = self.new_logs
        log_offset = self.log_offset
        mem_peak = self.mem_peak
        progress = self.progress
        stream_offset = self.stream_offset
        new_result_stream = self.new_result_stream
        flow_status: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow_status, Unset):
            flow_status = self.flow_status.to_dict()

        workflow_as_code_status: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.workflow_as_code_status, Unset):
            workflow_as_code_status = self.workflow_as_code_status.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if running is not UNSET:
            field_dict["running"] = running
        if completed is not UNSET:
            field_dict["completed"] = completed
        if new_logs is not UNSET:
            field_dict["new_logs"] = new_logs
        if log_offset is not UNSET:
            field_dict["log_offset"] = log_offset
        if mem_peak is not UNSET:
            field_dict["mem_peak"] = mem_peak
        if progress is not UNSET:
            field_dict["progress"] = progress
        if stream_offset is not UNSET:
            field_dict["stream_offset"] = stream_offset
        if new_result_stream is not UNSET:
            field_dict["new_result_stream"] = new_result_stream
        if flow_status is not UNSET:
            field_dict["flow_status"] = flow_status
        if workflow_as_code_status is not UNSET:
            field_dict["workflow_as_code_status"] = workflow_as_code_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_job_updates_response_200_flow_status import GetJobUpdatesResponse200FlowStatus
        from ..models.get_job_updates_response_200_workflow_as_code_status import (
            GetJobUpdatesResponse200WorkflowAsCodeStatus,
        )

        d = src_dict.copy()
        running = d.pop("running", UNSET)

        completed = d.pop("completed", UNSET)

        new_logs = d.pop("new_logs", UNSET)

        log_offset = d.pop("log_offset", UNSET)

        mem_peak = d.pop("mem_peak", UNSET)

        progress = d.pop("progress", UNSET)

        stream_offset = d.pop("stream_offset", UNSET)

        new_result_stream = d.pop("new_result_stream", UNSET)

        _flow_status = d.pop("flow_status", UNSET)
        flow_status: Union[Unset, GetJobUpdatesResponse200FlowStatus]
        if isinstance(_flow_status, Unset):
            flow_status = UNSET
        else:
            flow_status = GetJobUpdatesResponse200FlowStatus.from_dict(_flow_status)

        _workflow_as_code_status = d.pop("workflow_as_code_status", UNSET)
        workflow_as_code_status: Union[Unset, GetJobUpdatesResponse200WorkflowAsCodeStatus]
        if isinstance(_workflow_as_code_status, Unset):
            workflow_as_code_status = UNSET
        else:
            workflow_as_code_status = GetJobUpdatesResponse200WorkflowAsCodeStatus.from_dict(_workflow_as_code_status)

        get_job_updates_response_200 = cls(
            running=running,
            completed=completed,
            new_logs=new_logs,
            log_offset=log_offset,
            mem_peak=mem_peak,
            progress=progress,
            stream_offset=stream_offset,
            new_result_stream=new_result_stream,
            flow_status=flow_status,
            workflow_as_code_status=workflow_as_code_status,
        )

        get_job_updates_response_200.additional_properties = d
        return get_job_updates_response_200

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
