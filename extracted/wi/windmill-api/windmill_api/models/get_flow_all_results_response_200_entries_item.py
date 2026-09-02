import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_flow_all_results_response_200_entries_item_status import GetFlowAllResultsResponse200EntriesItemStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetFlowAllResultsResponse200EntriesItem")


@_attrs_define
class GetFlowAllResultsResponse200EntriesItem:
    """
    Attributes:
        job_id (str):
        label (str): human-readable label describing the job's position in the flow tree
        kind (str): job kind (script, flow, forloopflow, ...)
        depth (int): depth in the flow tree (0 for the root flow job)
        sibling_index (int): 1-based index of this job among siblings sharing the same step
        sibling_count (int): total number of siblings sharing the same step
        status (GetFlowAllResultsResponse200EntriesItemStatus):
        flow_step_id (Union[Unset, None, str]):
        step_path (Union[Unset, None, str]): materialized step path (e.g. "a/b")
        parent_module_type (Union[Unset, None, str]): parent module type (forloopflow, branchall, ...)
        success (Union[Unset, bool]):
        duration_ms (Union[Unset, int]):
        started_at (Union[Unset, datetime.datetime]):
        result_prefix (Union[Unset, str]): result JSON text truncated to the per-entry budget; absent until the job has
            completed
        result_length (Union[Unset, int]): full length in characters of the result JSON text (greater than the prefix
            length when truncated)
    """

    job_id: str
    label: str
    kind: str
    depth: int
    sibling_index: int
    sibling_count: int
    status: GetFlowAllResultsResponse200EntriesItemStatus
    flow_step_id: Union[Unset, None, str] = UNSET
    step_path: Union[Unset, None, str] = UNSET
    parent_module_type: Union[Unset, None, str] = UNSET
    success: Union[Unset, bool] = UNSET
    duration_ms: Union[Unset, int] = UNSET
    started_at: Union[Unset, datetime.datetime] = UNSET
    result_prefix: Union[Unset, str] = UNSET
    result_length: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_id = self.job_id
        label = self.label
        kind = self.kind
        depth = self.depth
        sibling_index = self.sibling_index
        sibling_count = self.sibling_count
        status = self.status.value

        flow_step_id = self.flow_step_id
        step_path = self.step_path
        parent_module_type = self.parent_module_type
        success = self.success
        duration_ms = self.duration_ms
        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        result_prefix = self.result_prefix
        result_length = self.result_length

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
                "label": label,
                "kind": kind,
                "depth": depth,
                "sibling_index": sibling_index,
                "sibling_count": sibling_count,
                "status": status,
            }
        )
        if flow_step_id is not UNSET:
            field_dict["flow_step_id"] = flow_step_id
        if step_path is not UNSET:
            field_dict["step_path"] = step_path
        if parent_module_type is not UNSET:
            field_dict["parent_module_type"] = parent_module_type
        if success is not UNSET:
            field_dict["success"] = success
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if result_prefix is not UNSET:
            field_dict["result_prefix"] = result_prefix
        if result_length is not UNSET:
            field_dict["result_length"] = result_length

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_id = d.pop("job_id")

        label = d.pop("label")

        kind = d.pop("kind")

        depth = d.pop("depth")

        sibling_index = d.pop("sibling_index")

        sibling_count = d.pop("sibling_count")

        status = GetFlowAllResultsResponse200EntriesItemStatus(d.pop("status"))

        flow_step_id = d.pop("flow_step_id", UNSET)

        step_path = d.pop("step_path", UNSET)

        parent_module_type = d.pop("parent_module_type", UNSET)

        success = d.pop("success", UNSET)

        duration_ms = d.pop("duration_ms", UNSET)

        _started_at = d.pop("started_at", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        result_prefix = d.pop("result_prefix", UNSET)

        result_length = d.pop("result_length", UNSET)

        get_flow_all_results_response_200_entries_item = cls(
            job_id=job_id,
            label=label,
            kind=kind,
            depth=depth,
            sibling_index=sibling_index,
            sibling_count=sibling_count,
            status=status,
            flow_step_id=flow_step_id,
            step_path=step_path,
            parent_module_type=parent_module_type,
            success=success,
            duration_ms=duration_ms,
            started_at=started_at,
            result_prefix=result_prefix,
            result_length=result_length,
        )

        get_flow_all_results_response_200_entries_item.additional_properties = d
        return get_flow_all_results_response_200_entries_item

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
