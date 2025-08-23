from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ai_agent_type import AiAgentType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_agent_input_transforms import AiAgentInputTransforms
    from ..models.ai_agent_tools_item import AiAgentToolsItem


T = TypeVar("T", bound="AiAgent")


@_attrs_define
class AiAgent:
    """
    Attributes:
        input_transforms (AiAgentInputTransforms):
        tools (List['AiAgentToolsItem']):
        type (AiAgentType):
        parallel (Union[Unset, bool]):
    """

    input_transforms: "AiAgentInputTransforms"
    tools: List["AiAgentToolsItem"]
    type: AiAgentType
    parallel: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_transforms = self.input_transforms.to_dict()

        tools = []
        for tools_item_data in self.tools:
            tools_item = tools_item_data.to_dict()

            tools.append(tools_item)

        type = self.type.value

        parallel = self.parallel

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input_transforms": input_transforms,
                "tools": tools,
                "type": type,
            }
        )
        if parallel is not UNSET:
            field_dict["parallel"] = parallel

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_agent_input_transforms import AiAgentInputTransforms
        from ..models.ai_agent_tools_item import AiAgentToolsItem

        d = src_dict.copy()
        input_transforms = AiAgentInputTransforms.from_dict(d.pop("input_transforms"))

        tools = []
        _tools = d.pop("tools")
        for tools_item_data in _tools:
            tools_item = AiAgentToolsItem.from_dict(tools_item_data)

            tools.append(tools_item)

        type = AiAgentType(d.pop("type"))

        parallel = d.pop("parallel", UNSET)

        ai_agent = cls(
            input_transforms=input_transforms,
            tools=tools,
            type=type,
            parallel=parallel,
        )

        ai_agent.additional_properties = d
        return ai_agent

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
