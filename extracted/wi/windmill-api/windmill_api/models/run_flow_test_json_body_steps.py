from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.run_flow_test_json_body_steps_additional_property import RunFlowTestJsonBodyStepsAdditionalProperty


T = TypeVar("T", bound="RunFlowTestJsonBodySteps")


@_attrs_define
class RunFlowTestJsonBodySteps:
    """step id -> override. A step inside a subflow is named by the path of step ids to it, `sub:inner` for step `inner` of
    the subflow that step `sub` calls.

    """

    additional_properties: Dict[str, "RunFlowTestJsonBodyStepsAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_flow_test_json_body_steps_additional_property import (
            RunFlowTestJsonBodyStepsAdditionalProperty,
        )

        d = src_dict.copy()
        run_flow_test_json_body_steps = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = RunFlowTestJsonBodyStepsAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        run_flow_test_json_body_steps.additional_properties = additional_properties
        return run_flow_test_json_body_steps

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "RunFlowTestJsonBodyStepsAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "RunFlowTestJsonBodyStepsAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
