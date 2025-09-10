from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_hub_flow_by_id_response_200_flow_value_preprocessor_module_timeout_type_0_type import (
    GetHubFlowByIdResponse200FlowValuePreprocessorModuleTimeoutType0Type,
)

T = TypeVar("T", bound="GetHubFlowByIdResponse200FlowValuePreprocessorModuleTimeoutType0")


@_attrs_define
class GetHubFlowByIdResponse200FlowValuePreprocessorModuleTimeoutType0:
    """
    Attributes:
        value (Any):
        type (GetHubFlowByIdResponse200FlowValuePreprocessorModuleTimeoutType0Type):
    """

    value: Any
    type: GetHubFlowByIdResponse200FlowValuePreprocessorModuleTimeoutType0Type
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        type = GetHubFlowByIdResponse200FlowValuePreprocessorModuleTimeoutType0Type(d.pop("type"))

        get_hub_flow_by_id_response_200_flow_value_preprocessor_module_timeout_type_0 = cls(
            value=value,
            type=type,
        )

        get_hub_flow_by_id_response_200_flow_value_preprocessor_module_timeout_type_0.additional_properties = d
        return get_hub_flow_by_id_response_200_flow_value_preprocessor_module_timeout_type_0

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
