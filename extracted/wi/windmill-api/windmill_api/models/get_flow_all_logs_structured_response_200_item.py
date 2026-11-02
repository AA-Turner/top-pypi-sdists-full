from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetFlowAllLogsStructuredResponse200Item")


@_attrs_define
class GetFlowAllLogsStructuredResponse200Item:
    """
    Attributes:
        job_id (str):
        label (str): human-readable label describing the job's position in the flow tree
        kind (str): job kind (script, flow, forloopflow, ...)
        depth (int): depth in the flow tree (0 for the root flow job)
        sibling_index (int): 1-based index of this job among siblings sharing the same step
        sibling_count (int): total number of siblings sharing the same step
        logs (str):
        flow_step_id (Union[Unset, None, str]):
        step_path (Union[Unset, None, str]): materialized step path (e.g. "a/b")
        parent_module_type (Union[Unset, None, str]): parent module type (forloopflow, branchall, ...)
    """

    job_id: str
    label: str
    kind: str
    depth: int
    sibling_index: int
    sibling_count: int
    logs: str
    flow_step_id: Union[Unset, None, str] = UNSET
    step_path: Union[Unset, None, str] = UNSET
    parent_module_type: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_id = self.job_id
        label = self.label
        kind = self.kind
        depth = self.depth
        sibling_index = self.sibling_index
        sibling_count = self.sibling_count
        logs = self.logs
        flow_step_id = self.flow_step_id
        step_path = self.step_path
        parent_module_type = self.parent_module_type

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
                "logs": logs,
            }
        )
        if flow_step_id is not UNSET:
            field_dict["flow_step_id"] = flow_step_id
        if step_path is not UNSET:
            field_dict["step_path"] = step_path
        if parent_module_type is not UNSET:
            field_dict["parent_module_type"] = parent_module_type

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

        logs = d.pop("logs")

        flow_step_id = d.pop("flow_step_id", UNSET)

        step_path = d.pop("step_path", UNSET)

        parent_module_type = d.pop("parent_module_type", UNSET)

        get_flow_all_logs_structured_response_200_item = cls(
            job_id=job_id,
            label=label,
            kind=kind,
            depth=depth,
            sibling_index=sibling_index,
            sibling_count=sibling_count,
            logs=logs,
            flow_step_id=flow_step_id,
            step_path=step_path,
            parent_module_type=parent_module_type,
        )

        get_flow_all_logs_structured_response_200_item.additional_properties = d
        return get_flow_all_logs_structured_response_200_item

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
