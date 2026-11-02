from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.token_analysis_issue_confidence import TokenAnalysisIssueConfidence
from ..models.token_analysis_issue_kind import TokenAnalysisIssueKind
from ..models.token_analysis_issue_severity import TokenAnalysisIssueSeverity

T = TypeVar("T", bound="TokenAnalysisIssue")


@_attrs_define
class TokenAnalysisIssue:
    """
    Attributes:
        kind (TokenAnalysisIssueKind):
        severity (TokenAnalysisIssueSeverity):
        confidence (TokenAnalysisIssueConfidence):
        title (str):
        detail (str):
    """

    kind: TokenAnalysisIssueKind
    severity: TokenAnalysisIssueSeverity
    confidence: TokenAnalysisIssueConfidence
    title: str
    detail: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        severity = self.severity.value

        confidence = self.confidence.value

        title = self.title

        detail = self.detail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "severity": severity,
                "confidence": confidence,
                "title": title,
                "detail": detail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = TokenAnalysisIssueKind(d.pop("kind"))

        severity = TokenAnalysisIssueSeverity(d.pop("severity"))

        confidence = TokenAnalysisIssueConfidence(d.pop("confidence"))

        title = d.pop("title")

        detail = d.pop("detail")

        token_analysis_issue = cls(
            kind=kind,
            severity=severity,
            confidence=confidence,
            title=title,
            detail=detail,
        )

        token_analysis_issue.additional_properties = d
        return token_analysis_issue

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
