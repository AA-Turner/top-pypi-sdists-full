from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.call_mcp_tool_response_200_content_item import CallMcpToolResponse200ContentItem
    from ..models.call_mcp_tool_response_200_structured_content import CallMcpToolResponse200StructuredContent


T = TypeVar("T", bound="CallMcpToolResponse200")


@_attrs_define
class CallMcpToolResponse200:
    """
    Attributes:
        content (Union[Unset, List['CallMcpToolResponse200ContentItem']]):
        structured_content (Union[Unset, CallMcpToolResponse200StructuredContent]):
        is_error (Union[Unset, bool]):
    """

    content: Union[Unset, List["CallMcpToolResponse200ContentItem"]] = UNSET
    structured_content: Union[Unset, "CallMcpToolResponse200StructuredContent"] = UNSET
    is_error: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.content, Unset):
            content = []
            for content_item_data in self.content:
                content_item = content_item_data.to_dict()

                content.append(content_item)

        structured_content: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.structured_content, Unset):
            structured_content = self.structured_content.to_dict()

        is_error = self.is_error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if structured_content is not UNSET:
            field_dict["structuredContent"] = structured_content
        if is_error is not UNSET:
            field_dict["isError"] = is_error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.call_mcp_tool_response_200_content_item import CallMcpToolResponse200ContentItem
        from ..models.call_mcp_tool_response_200_structured_content import CallMcpToolResponse200StructuredContent

        d = src_dict.copy()
        content = []
        _content = d.pop("content", UNSET)
        for content_item_data in _content or []:
            content_item = CallMcpToolResponse200ContentItem.from_dict(content_item_data)

            content.append(content_item)

        _structured_content = d.pop("structuredContent", UNSET)
        structured_content: Union[Unset, CallMcpToolResponse200StructuredContent]
        if isinstance(_structured_content, Unset):
            structured_content = UNSET
        else:
            structured_content = CallMcpToolResponse200StructuredContent.from_dict(_structured_content)

        is_error = d.pop("isError", UNSET)

        call_mcp_tool_response_200 = cls(
            content=content,
            structured_content=structured_content,
            is_error=is_error,
        )

        call_mcp_tool_response_200.additional_properties = d
        return call_mcp_tool_response_200

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
