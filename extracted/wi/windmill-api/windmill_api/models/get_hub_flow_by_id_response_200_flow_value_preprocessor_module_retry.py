from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_hub_flow_by_id_response_200_flow_value_preprocessor_module_retry_constant import (
        GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetryConstant,
    )
    from ..models.get_hub_flow_by_id_response_200_flow_value_preprocessor_module_retry_exponential import (
        GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetryExponential,
    )


T = TypeVar("T", bound="GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetry")


@_attrs_define
class GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetry:
    """
    Attributes:
        constant (Union[Unset, GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetryConstant]):
        exponential (Union[Unset, GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetryExponential]):
    """

    constant: Union[Unset, "GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetryConstant"] = UNSET
    exponential: Union[Unset, "GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetryExponential"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        constant: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.constant, Unset):
            constant = self.constant.to_dict()

        exponential: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.exponential, Unset):
            exponential = self.exponential.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if constant is not UNSET:
            field_dict["constant"] = constant
        if exponential is not UNSET:
            field_dict["exponential"] = exponential

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_hub_flow_by_id_response_200_flow_value_preprocessor_module_retry_constant import (
            GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetryConstant,
        )
        from ..models.get_hub_flow_by_id_response_200_flow_value_preprocessor_module_retry_exponential import (
            GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetryExponential,
        )

        d = src_dict.copy()
        _constant = d.pop("constant", UNSET)
        constant: Union[Unset, GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetryConstant]
        if isinstance(_constant, Unset):
            constant = UNSET
        else:
            constant = GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetryConstant.from_dict(_constant)

        _exponential = d.pop("exponential", UNSET)
        exponential: Union[Unset, GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetryExponential]
        if isinstance(_exponential, Unset):
            exponential = UNSET
        else:
            exponential = GetHubFlowByIdResponse200FlowValuePreprocessorModuleRetryExponential.from_dict(_exponential)

        get_hub_flow_by_id_response_200_flow_value_preprocessor_module_retry = cls(
            constant=constant,
            exponential=exponential,
        )

        get_hub_flow_by_id_response_200_flow_value_preprocessor_module_retry.additional_properties = d
        return get_hub_flow_by_id_response_200_flow_value_preprocessor_module_retry

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
