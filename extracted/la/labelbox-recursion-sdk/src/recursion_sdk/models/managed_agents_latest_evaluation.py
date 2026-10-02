from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_latest_evaluation_result import ManagedAgentsLatestEvaluationResult
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="ManagedAgentsLatestEvaluation")



@_attrs_define
class ManagedAgentsLatestEvaluation:
    """ Compact newest immutable evaluation projected onto a session-list row.

        Example:
            {'created_at': '2026-02-18T09:30:00Z', 'evaluation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'result':
                'pass'}

        Attributes:
            created_at (datetime.datetime): UTC timestamp when the newest evaluation was recorded.
            evaluation_id (UUID): Stable identity of the newest immutable evaluation for this session.
            result (ManagedAgentsLatestEvaluationResult): Overall pass, fail, or not-applicable verdict.
     """

    created_at: datetime.datetime
    evaluation_id: UUID
    result: ManagedAgentsLatestEvaluationResult





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        evaluation_id = str(self.evaluation_id)

        result = self.result.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created_at": created_at,
            "evaluation_id": evaluation_id,
            "result": result,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        evaluation_id = UUID(d.pop("evaluation_id"))




        result = ManagedAgentsLatestEvaluationResult(d.pop("result"))




        managed_agents_latest_evaluation = cls(
            created_at=created_at,
            evaluation_id=evaluation_id,
            result=result,
        )

        return managed_agents_latest_evaluation

