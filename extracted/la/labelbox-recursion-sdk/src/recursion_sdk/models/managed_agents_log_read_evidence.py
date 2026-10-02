from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_log_read_evidence_outcome import ManagedAgentsLogReadEvidenceOutcome
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsLogReadEvidence")



@_attrs_define
class ManagedAgentsLogReadEvidence:
    """ Evidence from one bounded Google Cloud Logging read attempted through an integration connection. It reports only the
    tested project, check time, and outcome; it contains no log entries or provider error body.

        Example:
            {'checked_at': '2026-02-18T09:30:00Z', 'outcome': 'entries', 'project_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            checked_at (datetime.datetime): Time of this explicit check; not continuous health.
            outcome (ManagedAgentsLogReadEvidenceOutcome): entries and empty both prove a successful read; other values do
                not.
            project_id (str): The single project explicitly tested.
     """

    checked_at: datetime.datetime
    outcome: ManagedAgentsLogReadEvidenceOutcome
    project_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        checked_at = self.checked_at.isoformat()

        outcome = self.outcome.value

        project_id = self.project_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "checked_at": checked_at,
            "outcome": outcome,
            "project_id": project_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        checked_at = datetime.datetime.fromisoformat(d.pop("checked_at"))




        outcome = ManagedAgentsLogReadEvidenceOutcome(d.pop("outcome"))




        project_id = d.pop("project_id")

        managed_agents_log_read_evidence = cls(
            checked_at=checked_at,
            outcome=outcome,
            project_id=project_id,
        )


        managed_agents_log_read_evidence.additional_properties = d
        return managed_agents_log_read_evidence

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
