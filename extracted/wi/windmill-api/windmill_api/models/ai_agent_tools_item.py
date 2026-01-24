from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_agent_tools_item_value_type_0 import AiAgentToolsItemValueType0
    from ..models.ai_agent_tools_item_value_type_1 import AiAgentToolsItemValueType1
    from ..models.ai_agent_tools_item_value_type_2 import AiAgentToolsItemValueType2


T = TypeVar("T", bound="AiAgentToolsItem")


@_attrs_define
class AiAgentToolsItem:
    """A tool available to an AI agent. Can be a flow module or an external MCP (Model Context Protocol) tool

    Attributes:
        id (str): Unique identifier for this tool. Cannot contain spaces - use underscores instead (e.g.,
            'get_user_data' not 'get user data')
        value (Union['AiAgentToolsItemValueType0', 'AiAgentToolsItemValueType1', 'AiAgentToolsItemValueType2']): The
            implementation of a tool. Can be a flow module (script/flow) or an MCP tool reference
        summary (Union[Unset, str]): Short description of what this tool does (shown to the AI)
    """

    id: str
    value: Union["AiAgentToolsItemValueType0", "AiAgentToolsItemValueType1", "AiAgentToolsItemValueType2"]
    summary: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.ai_agent_tools_item_value_type_0 import AiAgentToolsItemValueType0
        from ..models.ai_agent_tools_item_value_type_1 import AiAgentToolsItemValueType1

        id = self.id
        value: Dict[str, Any]

        if isinstance(self.value, AiAgentToolsItemValueType0):
            value = self.value.to_dict()

        elif isinstance(self.value, AiAgentToolsItemValueType1):
            value = self.value.to_dict()

        else:
            value = self.value.to_dict()

        summary = self.summary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "value": value,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_agent_tools_item_value_type_0 import AiAgentToolsItemValueType0
        from ..models.ai_agent_tools_item_value_type_1 import AiAgentToolsItemValueType1
        from ..models.ai_agent_tools_item_value_type_2 import AiAgentToolsItemValueType2

        d = src_dict.copy()
        id = d.pop("id")

        def _parse_value(
            data: object,
        ) -> Union["AiAgentToolsItemValueType0", "AiAgentToolsItemValueType1", "AiAgentToolsItemValueType2"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_0 = AiAgentToolsItemValueType0.from_dict(data)

                return value_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_1 = AiAgentToolsItemValueType1.from_dict(data)

                return value_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            value_type_2 = AiAgentToolsItemValueType2.from_dict(data)

            return value_type_2

        value = _parse_value(d.pop("value"))

        summary = d.pop("summary", UNSET)

        ai_agent_tools_item = cls(
            id=id,
            value=value,
            summary=summary,
        )

        ai_agent_tools_item.additional_properties = d
        return ai_agent_tools_item

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
