from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.token_analysis_finding import TokenAnalysisFinding
    from ..models.token_analysis_issue import TokenAnalysisIssue


T = TypeVar("T", bound="TokenAnalysisToolCall")


@_attrs_define
class TokenAnalysisToolCall:
    """
    Attributes:
        id (str):
        event_id (str):
        runtime_id (str):
        provider (None | str):
        tool_name (None | str):
        tool_call_id (None | str):
        observed_at_unix_millis (int):
        input_chars (int):
        output_chars (int):
        total_chars (int):
        estimated_input_tokens (int):
        estimated_output_tokens (int):
        estimated_total_tokens (int):
        estimated_savings_tokens (int):
        truncated (bool):
        parse_error (None | str):
        analysis_issues (list[TokenAnalysisIssue]):
        findings (list[TokenAnalysisFinding]):
        input_preview (str):
        output_preview (str):
        analyzer_version (int): Which rule set produced this row. Findings are never recomputed.
    """

    id: str
    event_id: str
    runtime_id: str
    provider: None | str
    tool_name: None | str
    tool_call_id: None | str
    observed_at_unix_millis: int
    input_chars: int
    output_chars: int
    total_chars: int
    estimated_input_tokens: int
    estimated_output_tokens: int
    estimated_total_tokens: int
    estimated_savings_tokens: int
    truncated: bool
    parse_error: None | str
    analysis_issues: list[TokenAnalysisIssue]
    findings: list[TokenAnalysisFinding]
    input_preview: str
    output_preview: str
    analyzer_version: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        event_id = self.event_id

        runtime_id = self.runtime_id

        provider: None | str
        provider = self.provider

        tool_name: None | str
        tool_name = self.tool_name

        tool_call_id: None | str
        tool_call_id = self.tool_call_id

        observed_at_unix_millis = self.observed_at_unix_millis

        input_chars = self.input_chars

        output_chars = self.output_chars

        total_chars = self.total_chars

        estimated_input_tokens = self.estimated_input_tokens

        estimated_output_tokens = self.estimated_output_tokens

        estimated_total_tokens = self.estimated_total_tokens

        estimated_savings_tokens = self.estimated_savings_tokens

        truncated = self.truncated

        parse_error: None | str
        parse_error = self.parse_error

        analysis_issues = []
        for analysis_issues_item_data in self.analysis_issues:
            analysis_issues_item = analysis_issues_item_data.to_dict()
            analysis_issues.append(analysis_issues_item)

        findings = []
        for findings_item_data in self.findings:
            findings_item = findings_item_data.to_dict()
            findings.append(findings_item)

        input_preview = self.input_preview

        output_preview = self.output_preview

        analyzer_version = self.analyzer_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "event_id": event_id,
                "runtime_id": runtime_id,
                "provider": provider,
                "tool_name": tool_name,
                "tool_call_id": tool_call_id,
                "observed_at_unix_millis": observed_at_unix_millis,
                "input_chars": input_chars,
                "output_chars": output_chars,
                "total_chars": total_chars,
                "estimated_input_tokens": estimated_input_tokens,
                "estimated_output_tokens": estimated_output_tokens,
                "estimated_total_tokens": estimated_total_tokens,
                "estimated_savings_tokens": estimated_savings_tokens,
                "truncated": truncated,
                "parse_error": parse_error,
                "analysis_issues": analysis_issues,
                "findings": findings,
                "input_preview": input_preview,
                "output_preview": output_preview,
                "analyzer_version": analyzer_version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.token_analysis_finding import TokenAnalysisFinding
        from ..models.token_analysis_issue import TokenAnalysisIssue

        d = dict(src_dict)
        id = d.pop("id")

        event_id = d.pop("event_id")

        runtime_id = d.pop("runtime_id")

        def _parse_provider(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        provider = _parse_provider(d.pop("provider"))

        def _parse_tool_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        tool_name = _parse_tool_name(d.pop("tool_name"))

        def _parse_tool_call_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        tool_call_id = _parse_tool_call_id(d.pop("tool_call_id"))

        observed_at_unix_millis = d.pop("observed_at_unix_millis")

        input_chars = d.pop("input_chars")

        output_chars = d.pop("output_chars")

        total_chars = d.pop("total_chars")

        estimated_input_tokens = d.pop("estimated_input_tokens")

        estimated_output_tokens = d.pop("estimated_output_tokens")

        estimated_total_tokens = d.pop("estimated_total_tokens")

        estimated_savings_tokens = d.pop("estimated_savings_tokens")

        truncated = d.pop("truncated")

        def _parse_parse_error(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        parse_error = _parse_parse_error(d.pop("parse_error"))

        analysis_issues = []
        _analysis_issues = d.pop("analysis_issues")
        for analysis_issues_item_data in _analysis_issues:
            analysis_issues_item = TokenAnalysisIssue.from_dict(
                analysis_issues_item_data
            )

            analysis_issues.append(analysis_issues_item)

        findings = []
        _findings = d.pop("findings")
        for findings_item_data in _findings:
            findings_item = TokenAnalysisFinding.from_dict(findings_item_data)

            findings.append(findings_item)

        input_preview = d.pop("input_preview")

        output_preview = d.pop("output_preview")

        analyzer_version = d.pop("analyzer_version")

        token_analysis_tool_call = cls(
            id=id,
            event_id=event_id,
            runtime_id=runtime_id,
            provider=provider,
            tool_name=tool_name,
            tool_call_id=tool_call_id,
            observed_at_unix_millis=observed_at_unix_millis,
            input_chars=input_chars,
            output_chars=output_chars,
            total_chars=total_chars,
            estimated_input_tokens=estimated_input_tokens,
            estimated_output_tokens=estimated_output_tokens,
            estimated_total_tokens=estimated_total_tokens,
            estimated_savings_tokens=estimated_savings_tokens,
            truncated=truncated,
            parse_error=parse_error,
            analysis_issues=analysis_issues,
            findings=findings,
            input_preview=input_preview,
            output_preview=output_preview,
            analyzer_version=analyzer_version,
        )

        token_analysis_tool_call.additional_properties = d
        return token_analysis_tool_call

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
