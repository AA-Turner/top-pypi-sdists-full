from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsFinding")



@_attrs_define
class ManagedAgentsFinding:
    """ One review comment bound to an exact changed line. Every finding must land on a path, side, and line present in the
    trusted diff manifest, and no two findings may target the same location, so a review cannot comment on code it was
    not shown.

        Example:
            {'body': 'example', 'evidence': 'example', 'line': 1, 'path': 'example', 'severity': 'example', 'side':
                'example'}

        Attributes:
            body (str): Reviewer comment published at this location. Required, and at most 16 KiB.
            evidence (str): Quoted code or diff excerpt the finding rests on. Required, and at most 8 KiB.
            line (int): Line number within the named side of the diff. Must be a line the reviewed diff actually changed.
            path (str): Repository-relative path of the commented file, at most 4096 bytes. Must name a file the reviewed
                diff changed.
            severity (str): How serious the finding is: low, medium, high, or critical.
            side (str): Which side of the diff the line belongs to: LEFT for a removed line, RIGHT for an added one.
     """

    body: str
    evidence: str
    line: int
    path: str
    severity: str
    side: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        body = self.body

        evidence = self.evidence

        line = self.line

        path = self.path

        severity = self.severity

        side = self.side


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "body": body,
            "evidence": evidence,
            "line": line,
            "path": path,
            "severity": severity,
            "side": side,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        body = d.pop("body")

        evidence = d.pop("evidence")

        line = d.pop("line")

        path = d.pop("path")

        severity = d.pop("severity")

        side = d.pop("side")

        managed_agents_finding = cls(
            body=body,
            evidence=evidence,
            line=line,
            path=path,
            severity=severity,
            side=side,
        )


        managed_agents_finding.additional_properties = d
        return managed_agents_finding

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
