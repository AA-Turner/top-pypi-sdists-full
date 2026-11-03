from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.call_ai_session_tool_json_body_context import CallAiSessionToolJsonBodyContext


T = TypeVar("T", bound="CallAiSessionToolJsonBody")


@_attrs_define
class CallAiSessionToolJsonBody:
    """
    Attributes:
        args (Union[Unset, Any]): the tool's arguments, as the model sent them
        context (Union[Unset, CallAiSessionToolJsonBodyContext]): browser-held state the tool reads
    """

    args: Union[Unset, Any] = UNSET
    context: Union[Unset, "CallAiSessionToolJsonBodyContext"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        args = self.args
        context: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if args is not UNSET:
            field_dict["args"] = args
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.call_ai_session_tool_json_body_context import CallAiSessionToolJsonBodyContext

        d = src_dict.copy()
        args = d.pop("args", UNSET)

        _context = d.pop("context", UNSET)
        context: Union[Unset, CallAiSessionToolJsonBodyContext]
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = CallAiSessionToolJsonBodyContext.from_dict(_context)

        call_ai_session_tool_json_body = cls(
            args=args,
            context=context,
        )

        call_ai_session_tool_json_body.additional_properties = d
        return call_ai_session_tool_json_body

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
