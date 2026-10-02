from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="ManagedAgentsNewestFailure")



@_attrs_define
class ManagedAgentsNewestFailure:
    """ One of the newest failing evaluations for a target agent, with deep-link evidence identity.

        Example:
            {'created_at': '2026-02-18T09:30:00Z', 'evaluation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'failed_criterion_keys': ['example'], 'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'target_session_available': True, 'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            created_at (datetime.datetime): UTC timestamp when the failing evaluation was recorded.
            evaluation_id (UUID): Immutable failing evaluation to open from the Overview.
            failed_criterion_keys (list[str]): Key-sorted rubric criteria that failed in this evaluation.
            snapshot_event_id (UUID): Canonical UUID transcript boundary to select when opening evidence; may be a current
                UUIDv7 or a retained legacy UUIDv4 event id.
            target_session_available (bool): Whether the same-organization target session is still available to open.
            target_session_id (UUID): Target session linked from the failure.
     """

    created_at: datetime.datetime
    evaluation_id: UUID
    failed_criterion_keys: list[str]
    snapshot_event_id: UUID
    target_session_available: bool
    target_session_id: UUID





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        evaluation_id = str(self.evaluation_id)

        failed_criterion_keys = self.failed_criterion_keys



        snapshot_event_id = str(self.snapshot_event_id)

        target_session_available = self.target_session_available

        target_session_id = str(self.target_session_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created_at": created_at,
            "evaluation_id": evaluation_id,
            "failed_criterion_keys": failed_criterion_keys,
            "snapshot_event_id": snapshot_event_id,
            "target_session_available": target_session_available,
            "target_session_id": target_session_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        evaluation_id = UUID(d.pop("evaluation_id"))




        failed_criterion_keys = cast(list[str], d.pop("failed_criterion_keys"))


        snapshot_event_id = UUID(d.pop("snapshot_event_id"))




        target_session_available = d.pop("target_session_available")

        target_session_id = UUID(d.pop("target_session_id"))




        managed_agents_newest_failure = cls(
            created_at=created_at,
            evaluation_id=evaluation_id,
            failed_criterion_keys=failed_criterion_keys,
            snapshot_event_id=snapshot_event_id,
            target_session_available=target_session_available,
            target_session_id=target_session_id,
        )

        return managed_agents_newest_failure

