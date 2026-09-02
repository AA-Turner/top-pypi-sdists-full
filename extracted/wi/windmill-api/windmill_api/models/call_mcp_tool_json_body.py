from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.call_mcp_tool_json_body_arguments import CallMcpToolJsonBodyArguments


T = TypeVar("T", bound="CallMcpToolJsonBody")


@_attrs_define
class CallMcpToolJsonBody:
    """
    Attributes:
        tool (str):
        arguments (Union[Unset, CallMcpToolJsonBodyArguments]):
        read_only (Union[Unset, bool]): set when the caller ran the tool without asking the user to
            confirm it; the call is refused unless the server's live
            listing marks the tool read-only
    """

    tool: str
    arguments: Union[Unset, "CallMcpToolJsonBodyArguments"] = UNSET
    read_only: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tool = self.tool
        arguments: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.arguments, Unset):
            arguments = self.arguments.to_dict()

        read_only = self.read_only

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tool": tool,
            }
        )
        if arguments is not UNSET:
            field_dict["arguments"] = arguments
        if read_only is not UNSET:
            field_dict["read_only"] = read_only

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.call_mcp_tool_json_body_arguments import CallMcpToolJsonBodyArguments

        d = src_dict.copy()
        tool = d.pop("tool")

        _arguments = d.pop("arguments", UNSET)
        arguments: Union[Unset, CallMcpToolJsonBodyArguments]
        if isinstance(_arguments, Unset):
            arguments = UNSET
        else:
            arguments = CallMcpToolJsonBodyArguments.from_dict(_arguments)

        read_only = d.pop("read_only", UNSET)

        call_mcp_tool_json_body = cls(
            tool=tool,
            arguments=arguments,
            read_only=read_only,
        )

        call_mcp_tool_json_body.additional_properties = d
        return call_mcp_tool_json_body

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
