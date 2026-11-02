from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.token_analysis_tool_call import TokenAnalysisToolCall


T = TypeVar("T", bound="TokenAnalysisDetail")


@_attrs_define
class TokenAnalysisDetail:
    """
    Attributes:
        call (TokenAnalysisToolCall):
        input_text (str):
        output_text (str):
    """

    call: TokenAnalysisToolCall
    input_text: str
    output_text: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        call = self.call.to_dict()

        input_text = self.input_text

        output_text = self.output_text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "call": call,
                "input_text": input_text,
                "output_text": output_text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.token_analysis_tool_call import TokenAnalysisToolCall

        d = dict(src_dict)
        call = TokenAnalysisToolCall.from_dict(d.pop("call"))

        input_text = d.pop("input_text")

        output_text = d.pop("output_text")

        token_analysis_detail = cls(
            call=call,
            input_text=input_text,
            output_text=output_text,
        )

        token_analysis_detail.additional_properties = d
        return token_analysis_detail

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
