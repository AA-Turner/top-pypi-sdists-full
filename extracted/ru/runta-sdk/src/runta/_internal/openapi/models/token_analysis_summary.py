from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TokenAnalysisSummary")


@_attrs_define
class TokenAnalysisSummary:
    """Totals over everything the filter selects, not merely the page returned.

    Attributes:
        total_calls (int):
        calls_with_findings (int):
        calls_with_analysis_issues (int):
        estimated_tokens (int):
        estimated_savings_tokens (int):
        truncated_calls (int):
    """

    total_calls: int
    calls_with_findings: int
    calls_with_analysis_issues: int
    estimated_tokens: int
    estimated_savings_tokens: int
    truncated_calls: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_calls = self.total_calls

        calls_with_findings = self.calls_with_findings

        calls_with_analysis_issues = self.calls_with_analysis_issues

        estimated_tokens = self.estimated_tokens

        estimated_savings_tokens = self.estimated_savings_tokens

        truncated_calls = self.truncated_calls

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_calls": total_calls,
                "calls_with_findings": calls_with_findings,
                "calls_with_analysis_issues": calls_with_analysis_issues,
                "estimated_tokens": estimated_tokens,
                "estimated_savings_tokens": estimated_savings_tokens,
                "truncated_calls": truncated_calls,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_calls = d.pop("total_calls")

        calls_with_findings = d.pop("calls_with_findings")

        calls_with_analysis_issues = d.pop("calls_with_analysis_issues")

        estimated_tokens = d.pop("estimated_tokens")

        estimated_savings_tokens = d.pop("estimated_savings_tokens")

        truncated_calls = d.pop("truncated_calls")

        token_analysis_summary = cls(
            total_calls=total_calls,
            calls_with_findings=calls_with_findings,
            calls_with_analysis_issues=calls_with_analysis_issues,
            estimated_tokens=estimated_tokens,
            estimated_savings_tokens=estimated_savings_tokens,
            truncated_calls=truncated_calls,
        )

        token_analysis_summary.additional_properties = d
        return token_analysis_summary

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
