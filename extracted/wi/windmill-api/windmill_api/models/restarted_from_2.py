from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.restarted_from_2_branch_chosen import RestartedFrom2BranchChosen


T = TypeVar("T", bound="RestartedFrom2")


@_attrs_define
class RestartedFrom2:
    """
    Attributes:
        flow_job_id (Union[Unset, str]):
        step_id (Union[Unset, str]):
        branch_or_iteration_n (Union[Unset, int]): 0-based iteration index for ForLoop / branch index for BranchAll.
            Iterations 0..n-1 are preserved; iteration n is restarted.
        flow_version (Union[Unset, int]):
        branch_chosen (Union[Unset, RestartedFrom2BranchChosen]): For BranchOne nested restart — the branch that was
            originally chosen, used to lock branch evaluation.
        nested (Union[Unset, Any]): When set, the worker spawns the child for `step_id` as a `RestartedFlow` against
            `nested.flow_job_id` instead of fresh-launching it.
        failed_only (Union[Unset, bool]): For a parallel for-loop or branch-all at `step_id`, keep the iterations
            (branches) that succeeded and rerun only the others.
        from_failed_step (Union[Unset, bool]): With `failed_only`, resume each failed iteration (branch) at the step
            where it failed rather than rerunning it from its first step.
    """

    flow_job_id: Union[Unset, str] = UNSET
    step_id: Union[Unset, str] = UNSET
    branch_or_iteration_n: Union[Unset, int] = UNSET
    flow_version: Union[Unset, int] = UNSET
    branch_chosen: Union[Unset, "RestartedFrom2BranchChosen"] = UNSET
    nested: Union[Unset, Any] = UNSET
    failed_only: Union[Unset, bool] = UNSET
    from_failed_step: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        flow_job_id = self.flow_job_id
        step_id = self.step_id
        branch_or_iteration_n = self.branch_or_iteration_n
        flow_version = self.flow_version
        branch_chosen: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.branch_chosen, Unset):
            branch_chosen = self.branch_chosen.to_dict()

        nested = self.nested
        failed_only = self.failed_only
        from_failed_step = self.from_failed_step

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if flow_job_id is not UNSET:
            field_dict["flow_job_id"] = flow_job_id
        if step_id is not UNSET:
            field_dict["step_id"] = step_id
        if branch_or_iteration_n is not UNSET:
            field_dict["branch_or_iteration_n"] = branch_or_iteration_n
        if flow_version is not UNSET:
            field_dict["flow_version"] = flow_version
        if branch_chosen is not UNSET:
            field_dict["branch_chosen"] = branch_chosen
        if nested is not UNSET:
            field_dict["nested"] = nested
        if failed_only is not UNSET:
            field_dict["failed_only"] = failed_only
        if from_failed_step is not UNSET:
            field_dict["from_failed_step"] = from_failed_step

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.restarted_from_2_branch_chosen import RestartedFrom2BranchChosen

        d = src_dict.copy()
        flow_job_id = d.pop("flow_job_id", UNSET)

        step_id = d.pop("step_id", UNSET)

        branch_or_iteration_n = d.pop("branch_or_iteration_n", UNSET)

        flow_version = d.pop("flow_version", UNSET)

        _branch_chosen = d.pop("branch_chosen", UNSET)
        branch_chosen: Union[Unset, RestartedFrom2BranchChosen]
        if isinstance(_branch_chosen, Unset):
            branch_chosen = UNSET
        else:
            branch_chosen = RestartedFrom2BranchChosen.from_dict(_branch_chosen)

        nested = d.pop("nested", UNSET)

        failed_only = d.pop("failed_only", UNSET)

        from_failed_step = d.pop("from_failed_step", UNSET)

        restarted_from_2 = cls(
            flow_job_id=flow_job_id,
            step_id=step_id,
            branch_or_iteration_n=branch_or_iteration_n,
            flow_version=flow_version,
            branch_chosen=branch_chosen,
            nested=nested,
            failed_only=failed_only,
            from_failed_step=from_failed_step,
        )

        restarted_from_2.additional_properties = d
        return restarted_from_2

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
