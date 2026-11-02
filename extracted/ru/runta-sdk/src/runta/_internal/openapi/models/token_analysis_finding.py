from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.token_analysis_finding_confidence import TokenAnalysisFindingConfidence
from ..models.token_analysis_finding_kind import TokenAnalysisFindingKind
from ..models.token_analysis_finding_severity import TokenAnalysisFindingSeverity

T = TypeVar("T", bound="TokenAnalysisFinding")


@_attrs_define
class TokenAnalysisFinding:
    """
    Attributes:
        kind (TokenAnalysisFindingKind):
        severity (TokenAnalysisFindingSeverity):
        confidence (TokenAnalysisFindingConfidence):
        title (str):
        detail (str):
        estimated_savings_tokens (int):
    """

    kind: TokenAnalysisFindingKind
    severity: TokenAnalysisFindingSeverity
    confidence: TokenAnalysisFindingConfidence
    title: str
    detail: str
    estimated_savings_tokens: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        severity = self.severity.value

        confidence = self.confidence.value

        title = self.title

        detail = self.detail

        estimated_savings_tokens = self.estimated_savings_tokens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "severity": severity,
                "confidence": confidence,
                "title": title,
                "detail": detail,
                "estimated_savings_tokens": estimated_savings_tokens,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = TokenAnalysisFindingKind(d.pop("kind"))

        severity = TokenAnalysisFindingSeverity(d.pop("severity"))

        confidence = TokenAnalysisFindingConfidence(d.pop("confidence"))

        title = d.pop("title")

        detail = d.pop("detail")

        estimated_savings_tokens = d.pop("estimated_savings_tokens")

        token_analysis_finding = cls(
            kind=kind,
            severity=severity,
            confidence=confidence,
            title=title,
            detail=detail,
            estimated_savings_tokens=estimated_savings_tokens,
        )

        token_analysis_finding.additional_properties = d
        return token_analysis_finding

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
