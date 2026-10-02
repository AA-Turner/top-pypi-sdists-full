from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tool_execute_request_arguments import ToolExecuteRequestArguments


T = TypeVar("T", bound="ToolExecuteRequest")


@_attrs_define
class ToolExecuteRequest:
    """
    Attributes:
        tool (str): Name of the tool to execute.
        arguments (Union[Unset, ToolExecuteRequestArguments]): Tool arguments.
    """

    tool: str
    arguments: Union[Unset, "ToolExecuteRequestArguments"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tool = self.tool

        arguments: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.arguments, Unset):
            arguments = self.arguments.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tool": tool,
            }
        )
        if arguments is not UNSET:
            field_dict["arguments"] = arguments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_execute_request_arguments import ToolExecuteRequestArguments

        d = dict(src_dict)
        tool = d.pop("tool")

        _arguments = d.pop("arguments", UNSET)
        arguments: Union[Unset, ToolExecuteRequestArguments]
        if isinstance(_arguments, Unset):
            arguments = UNSET
        else:
            arguments = ToolExecuteRequestArguments.from_dict(_arguments)

        tool_execute_request = cls(
            tool=tool,
            arguments=arguments,
        )

        tool_execute_request.additional_properties = d
        return tool_execute_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
