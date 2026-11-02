from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.run_flow_dependencies_async_json_body_flow_value import RunFlowDependenciesAsyncJsonBodyFlowValue


T = TypeVar("T", bound="RunFlowDependenciesAsyncJsonBody")


@_attrs_define
class RunFlowDependenciesAsyncJsonBody:
    """
    Attributes:
        path (str):
        flow_value (RunFlowDependenciesAsyncJsonBodyFlowValue): The flow structure containing modules and optional
            preprocessor/failure handlers
    """

    path: str
    flow_value: "RunFlowDependenciesAsyncJsonBodyFlowValue"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        flow_value = self.flow_value.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "flow_value": flow_value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_flow_dependencies_async_json_body_flow_value import RunFlowDependenciesAsyncJsonBodyFlowValue

        d = src_dict.copy()
        path = d.pop("path")

        flow_value = RunFlowDependenciesAsyncJsonBodyFlowValue.from_dict(d.pop("flow_value"))

        run_flow_dependencies_async_json_body = cls(
            path=path,
            flow_value=flow_value,
        )

        run_flow_dependencies_async_json_body.additional_properties = d
        return run_flow_dependencies_async_json_body

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
