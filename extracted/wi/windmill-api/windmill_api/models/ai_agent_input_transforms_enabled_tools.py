from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AiAgentInputTransformsEnabledTools")


@_attrs_define
class AiAgentInputTransformsEnabledTools:
    """Array of strings naming which of the tools configured in `tools` the agent may call
    this run. Leaving it unset carries every one of them; an empty array carries none.
    A tool is named as the model is shown it. An entry the model is shown nothing of is
    named by what identifies it instead: an MCP server by its resource path, carrying
    every tool it exposes (which of them stays that entry's include_tools/exclude_tools),
    and a websearch entry by the reserved name '__wm_web_search', whatever summary it carries
    (no tool may take that name).
    Example: ['get_user', 'u/admin/github_mcp', '__wm_web_search']

    """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ai_agent_input_transforms_enabled_tools = cls()

        ai_agent_input_transforms_enabled_tools.additional_properties = d
        return ai_agent_input_transforms_enabled_tools

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
