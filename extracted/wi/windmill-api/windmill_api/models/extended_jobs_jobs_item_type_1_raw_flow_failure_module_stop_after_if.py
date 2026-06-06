from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtendedJobsJobsItemType1RawFlowFailureModuleStopAfterIf")


@_attrs_define
class ExtendedJobsJobsItemType1RawFlowFailureModuleStopAfterIf:
    """Early termination condition for a module

    Attributes:
        expr (str): JavaScript expression evaluated after the module runs. Can use 'result' (step's result) or
            'flow_input'. Return true to stop
        skip_if_stopped (Union[Unset, bool]): If true, following steps are skipped when this condition triggers
        error_message (Union[Unset, None, str]): Custom error message when stopping with an error. Mutually exclusive
            with skip_if_stopped. If set to a non-empty string, the flow stops with this error. If empty string, a default
            error message is used. If null or omitted, no error is raised.
        error_include_result (Union[Unset, bool]): When stopping with an error (error_message set), embed the stopping
            step's own result inside the raised error object (as error.result) instead of discarding it. The top-level
            result stays { error }. Defaults to false.
    """

    expr: str
    skip_if_stopped: Union[Unset, bool] = UNSET
    error_message: Union[Unset, None, str] = UNSET
    error_include_result: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        expr = self.expr
        skip_if_stopped = self.skip_if_stopped
        error_message = self.error_message
        error_include_result = self.error_include_result

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expr": expr,
            }
        )
        if skip_if_stopped is not UNSET:
            field_dict["skip_if_stopped"] = skip_if_stopped
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_include_result is not UNSET:
            field_dict["error_include_result"] = error_include_result

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expr = d.pop("expr")

        skip_if_stopped = d.pop("skip_if_stopped", UNSET)

        error_message = d.pop("error_message", UNSET)

        error_include_result = d.pop("error_include_result", UNSET)

        extended_jobs_jobs_item_type_1_raw_flow_failure_module_stop_after_if = cls(
            expr=expr,
            skip_if_stopped=skip_if_stopped,
            error_message=error_message,
            error_include_result=error_include_result,
        )

        extended_jobs_jobs_item_type_1_raw_flow_failure_module_stop_after_if.additional_properties = d
        return extended_jobs_jobs_item_type_1_raw_flow_failure_module_stop_after_if

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
