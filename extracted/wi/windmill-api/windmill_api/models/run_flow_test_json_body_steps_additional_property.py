from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunFlowTestJsonBodyStepsAdditionalProperty")


@_attrs_define
class RunFlowTestJsonBodyStepsAdditionalProperty:
    """
    Attributes:
        return_value (Union[Unset, Any]): the step is skipped and returns this value
        function (Union[Unset, str]): name of a function of the code of `caller_job_id` that runs instead of the step
            (exported, in TypeScript)
    """

    return_value: Union[Unset, Any] = UNSET
    function: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return_value = self.return_value
        function = self.function

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if return_value is not UNSET:
            field_dict["return_value"] = return_value
        if function is not UNSET:
            field_dict["function"] = function

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        return_value = d.pop("return_value", UNSET)

        function = d.pop("function", UNSET)

        run_flow_test_json_body_steps_additional_property = cls(
            return_value=return_value,
            function=function,
        )

        run_flow_test_json_body_steps_additional_property.additional_properties = d
        return run_flow_test_json_body_steps_additional_property

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
