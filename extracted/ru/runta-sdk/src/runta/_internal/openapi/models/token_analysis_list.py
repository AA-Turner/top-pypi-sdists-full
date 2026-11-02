from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.token_analysis_summary import TokenAnalysisSummary
    from ..models.token_analysis_tool_call import TokenAnalysisToolCall


T = TypeVar("T", bound="TokenAnalysisList")


@_attrs_define
class TokenAnalysisList:
    """
    Attributes:
        calls (list[TokenAnalysisToolCall]):
        summary (TokenAnalysisSummary): Totals over everything the filter selects, not merely the page returned.
        next_page_token (None | str):
    """

    calls: list[TokenAnalysisToolCall]
    summary: TokenAnalysisSummary
    next_page_token: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        calls = []
        for calls_item_data in self.calls:
            calls_item = calls_item_data.to_dict()
            calls.append(calls_item)

        summary = self.summary.to_dict()

        next_page_token: None | str
        next_page_token = self.next_page_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "calls": calls,
                "summary": summary,
                "next_page_token": next_page_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.token_analysis_summary import TokenAnalysisSummary
        from ..models.token_analysis_tool_call import TokenAnalysisToolCall

        d = dict(src_dict)
        calls = []
        _calls = d.pop("calls")
        for calls_item_data in _calls:
            calls_item = TokenAnalysisToolCall.from_dict(calls_item_data)

            calls.append(calls_item)

        summary = TokenAnalysisSummary.from_dict(d.pop("summary"))

        def _parse_next_page_token(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_page_token = _parse_next_page_token(d.pop("next_page_token"))

        token_analysis_list = cls(
            calls=calls,
            summary=summary,
            next_page_token=next_page_token,
        )

        token_analysis_list.additional_properties = d
        return token_analysis_list

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
