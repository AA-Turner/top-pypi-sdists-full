from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flow_status_module_agent_actions_item_type_2_type import FlowStatusModuleAgentActionsItemType2Type

T = TypeVar("T", bound="FlowStatusModuleAgentActionsItemType2")


@_attrs_define
class FlowStatusModuleAgentActionsItemType2:
    """
    Attributes:
        type (FlowStatusModuleAgentActionsItemType2Type):
    """

    type: FlowStatusModuleAgentActionsItemType2Type
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = FlowStatusModuleAgentActionsItemType2Type(d.pop("type"))

        flow_status_module_agent_actions_item_type_2 = cls(
            type=type,
        )

        flow_status_module_agent_actions_item_type_2.additional_properties = d
        return flow_status_module_agent_actions_item_type_2

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
