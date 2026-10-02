from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_finding import ManagedAgentsFinding





T = TypeVar("T", bound="ManagedAgentsPullRequestReviewResult")



@_attrs_define
class ManagedAgentsPullRequestReviewResult:
    """ One agent's review of a pull request: a summary, a verdict, and the line-level findings. It is returned only after
    every claimed location has been rebound to the trusted exact-SHA diff manifest.

        Example:
            {'findings': [{'body': 'example', 'evidence': 'example', 'line': 1, 'path': 'example', 'severity': 'example',
                'side': 'example'}], 'summary': 'example', 'verdict': 'example'}

        Attributes:
            findings (list[ManagedAgentsFinding] | None): Line-level comments, at most 100, each bound to a line the
                reviewed diff changed.
            summary (str): Prose summary of the review. Required, and at most 4 KiB.
            verdict (str): no_findings when the review raised nothing, comment when it did. no_findings must carry an empty
                findings list, and comment requires at least one finding.
     """

    findings: list[ManagedAgentsFinding] | None
    summary: str
    verdict: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_finding import ManagedAgentsFinding # noqa: PLC0415
        findings: list[dict[str, Any]] | None
        if isinstance(self.findings, list):
            findings = []
            for findings_type_0_item_data in self.findings:
                findings_type_0_item = findings_type_0_item_data.to_dict()
                findings.append(findings_type_0_item)


        else:
            findings = self.findings

        summary = self.summary

        verdict = self.verdict


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "findings": findings,
            "summary": summary,
            "verdict": verdict,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_finding import ManagedAgentsFinding # noqa: PLC0415
        d = dict(src_dict)
        def _parse_findings(data: object) -> list[ManagedAgentsFinding] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                findings_type_0 = []
                _findings_type_0 = data
                for findings_type_0_item_data in (_findings_type_0):
                    findings_type_0_item = ManagedAgentsFinding.from_dict(findings_type_0_item_data)



                    findings_type_0.append(findings_type_0_item)

                return findings_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsFinding] | None, data)

        findings = _parse_findings(d.pop("findings"))


        summary = d.pop("summary")

        verdict = d.pop("verdict")

        managed_agents_pull_request_review_result = cls(
            findings=findings,
            summary=summary,
            verdict=verdict,
        )


        managed_agents_pull_request_review_result.additional_properties = d
        return managed_agents_pull_request_review_result

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
