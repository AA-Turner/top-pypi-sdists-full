from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.restart_flow_at_step_json_body_nested_path_item import RestartFlowAtStepJsonBodyNestedPathItem


T = TypeVar("T", bound="RestartFlowAtStepJsonBody")


@_attrs_define
class RestartFlowAtStepJsonBody:
    """
    Attributes:
        step_id (str): top-level step id to restart the flow from (or the outermost container when restarting at a
            nested step)
        branch_or_iteration_n (Union[Unset, int]): for branchall or loop at the top level, the iteration at which the
            flow should restart (optional)
        flow_version (Union[Unset, int]): specific flow version to use for restart (optional, uses current version if
            not specified)
        failed_only (Union[Unset, bool]): for a parallel for-loop or branch-all at the restart point (`step_id`, or the
            last `nested_path` entry), keep the iterations (branches) that succeeded and rerun only the others from their
            first step, each in its original position. Cannot be combined with an iteration to restart at on that same step.
        from_failed_step (Union[Unset, bool]): with `failed_only`, resume each failed iteration (branch) at the step
            where it failed, keeping the steps before it, rather than rerunning it from its first step.
        nested_path (Union[Unset, List['RestartFlowAtStepJsonBodyNestedPathItem']]): path of additional steps to descend
            into AFTER `step_id`. Each entry represents one level of nesting inside the spawned child of the previous
            level's container (BranchOne / sequential ForLoop iteration / Subflow). When non-empty, the actual restart point
            is the LAST entry's step_id.
    """

    step_id: str
    branch_or_iteration_n: Union[Unset, int] = UNSET
    flow_version: Union[Unset, int] = UNSET
    failed_only: Union[Unset, bool] = UNSET
    from_failed_step: Union[Unset, bool] = UNSET
    nested_path: Union[Unset, List["RestartFlowAtStepJsonBodyNestedPathItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        step_id = self.step_id
        branch_or_iteration_n = self.branch_or_iteration_n
        flow_version = self.flow_version
        failed_only = self.failed_only
        from_failed_step = self.from_failed_step
        nested_path: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.nested_path, Unset):
            nested_path = []
            for nested_path_item_data in self.nested_path:
                nested_path_item = nested_path_item_data.to_dict()

                nested_path.append(nested_path_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "step_id": step_id,
            }
        )
        if branch_or_iteration_n is not UNSET:
            field_dict["branch_or_iteration_n"] = branch_or_iteration_n
        if flow_version is not UNSET:
            field_dict["flow_version"] = flow_version
        if failed_only is not UNSET:
            field_dict["failed_only"] = failed_only
        if from_failed_step is not UNSET:
            field_dict["from_failed_step"] = from_failed_step
        if nested_path is not UNSET:
            field_dict["nested_path"] = nested_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.restart_flow_at_step_json_body_nested_path_item import RestartFlowAtStepJsonBodyNestedPathItem

        d = src_dict.copy()
        step_id = d.pop("step_id")

        branch_or_iteration_n = d.pop("branch_or_iteration_n", UNSET)

        flow_version = d.pop("flow_version", UNSET)

        failed_only = d.pop("failed_only", UNSET)

        from_failed_step = d.pop("from_failed_step", UNSET)

        nested_path = []
        _nested_path = d.pop("nested_path", UNSET)
        for nested_path_item_data in _nested_path or []:
            nested_path_item = RestartFlowAtStepJsonBodyNestedPathItem.from_dict(nested_path_item_data)

            nested_path.append(nested_path_item)

        restart_flow_at_step_json_body = cls(
            step_id=step_id,
            branch_or_iteration_n=branch_or_iteration_n,
            flow_version=flow_version,
            failed_only=failed_only,
            from_failed_step=from_failed_step,
            nested_path=nested_path,
        )

        restart_flow_at_step_json_body.additional_properties = d
        return restart_flow_at_step_json_body

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
