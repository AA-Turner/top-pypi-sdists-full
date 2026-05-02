from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RestartFlowAtStepJsonBodyNestedPathItem")


@_attrs_define
class RestartFlowAtStepJsonBodyNestedPathItem:
    """
    Attributes:
        step_id (str): step id at this nesting level
        branch_or_iteration_n (Union[Unset, int]): for ForLoop containers, the iteration to restart at (0-based;
            iterations 0..n-1 are preserved)
    """

    step_id: str
    branch_or_iteration_n: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        step_id = self.step_id
        branch_or_iteration_n = self.branch_or_iteration_n

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "step_id": step_id,
            }
        )
        if branch_or_iteration_n is not UNSET:
            field_dict["branch_or_iteration_n"] = branch_or_iteration_n

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        step_id = d.pop("step_id")

        branch_or_iteration_n = d.pop("branch_or_iteration_n", UNSET)

        restart_flow_at_step_json_body_nested_path_item = cls(
            step_id=step_id,
            branch_or_iteration_n=branch_or_iteration_n,
        )

        restart_flow_at_step_json_body_nested_path_item.additional_properties = d
        return restart_flow_at_step_json_body_nested_path_item

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
