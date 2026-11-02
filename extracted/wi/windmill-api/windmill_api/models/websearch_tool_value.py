from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.websearch_tool_value_tool_type import WebsearchToolValueToolType

T = TypeVar("T", bound="WebsearchToolValue")


@_attrs_define
class WebsearchToolValue:
    """A tool implemented as a websearch tool. The AI can call this like any other websearch tool

    Attributes:
        tool_type (WebsearchToolValueToolType):
    """

    tool_type: WebsearchToolValueToolType
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tool_type = self.tool_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tool_type": tool_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tool_type = WebsearchToolValueToolType(d.pop("tool_type"))

        websearch_tool_value = cls(
            tool_type=tool_type,
        )

        websearch_tool_value.additional_properties = d
        return websearch_tool_value

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
