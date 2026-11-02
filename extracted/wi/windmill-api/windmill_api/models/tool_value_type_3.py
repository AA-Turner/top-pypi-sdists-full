from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tool_value_type_3_tool_type import ToolValueType3ToolType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ToolValueType3")


@_attrs_define
class ToolValueType3:
    """Built-in tool the AI calls as ask_question: the agent stops, releasing its worker, until someone answers from the
    flow's run page or chat or the question times out, then resumes with the answer as the tool result.

        Attributes:
            tool_type (ToolValueType3ToolType):
            timeout (Union[Unset, int]): Seconds to wait for an answer before the question is reported to the AI as timed
                out. Defaults to 1800.
    """

    tool_type: ToolValueType3ToolType
    timeout: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tool_type = self.tool_type.value

        timeout = self.timeout

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tool_type": tool_type,
            }
        )
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tool_type = ToolValueType3ToolType(d.pop("tool_type"))

        timeout = d.pop("timeout", UNSET)

        tool_value_type_3 = cls(
            tool_type=tool_type,
            timeout=timeout,
        )

        tool_value_type_3.additional_properties = d
        return tool_value_type_3

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
