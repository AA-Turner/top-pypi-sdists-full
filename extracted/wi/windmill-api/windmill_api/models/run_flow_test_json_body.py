from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_flow_test_json_body_args import RunFlowTestJsonBodyArgs
    from ..models.run_flow_test_json_body_steps import RunFlowTestJsonBodySteps


T = TypeVar("T", bound="RunFlowTestJsonBody")


@_attrs_define
class RunFlowTestJsonBody:
    """
    Attributes:
        args (Union[Unset, RunFlowTestJsonBodyArgs]): The arguments to pass to the script or flow
        steps (Union[Unset, RunFlowTestJsonBodySteps]): step id -> override. A step inside a subflow is named by the
            path of step ids to it, `sub:inner` for step `inner` of the subflow that step `sub` calls.
        caller_job_id (Union[Unset, str]): the job whose code defines the replacing functions, usually the calling test;
            a script run or a script preview. Required with a `function` override.
    """

    args: Union[Unset, "RunFlowTestJsonBodyArgs"] = UNSET
    steps: Union[Unset, "RunFlowTestJsonBodySteps"] = UNSET
    caller_job_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args.to_dict()

        steps: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.steps, Unset):
            steps = self.steps.to_dict()

        caller_job_id = self.caller_job_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if args is not UNSET:
            field_dict["args"] = args
        if steps is not UNSET:
            field_dict["steps"] = steps
        if caller_job_id is not UNSET:
            field_dict["caller_job_id"] = caller_job_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_flow_test_json_body_args import RunFlowTestJsonBodyArgs
        from ..models.run_flow_test_json_body_steps import RunFlowTestJsonBodySteps

        d = src_dict.copy()
        _args = d.pop("args", UNSET)
        args: Union[Unset, RunFlowTestJsonBodyArgs]
        if isinstance(_args, Unset):
            args = UNSET
        else:
            args = RunFlowTestJsonBodyArgs.from_dict(_args)

        _steps = d.pop("steps", UNSET)
        steps: Union[Unset, RunFlowTestJsonBodySteps]
        if isinstance(_steps, Unset):
            steps = UNSET
        else:
            steps = RunFlowTestJsonBodySteps.from_dict(_steps)

        caller_job_id = d.pop("caller_job_id", UNSET)

        run_flow_test_json_body = cls(
            args=args,
            steps=steps,
            caller_job_id=caller_job_id,
        )

        run_flow_test_json_body.additional_properties = d
        return run_flow_test_json_body

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
