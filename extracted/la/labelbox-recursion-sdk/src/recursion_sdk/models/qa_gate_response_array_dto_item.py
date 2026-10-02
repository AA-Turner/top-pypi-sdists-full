from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.qa_gate_response_array_dto_item_blocked_stage import QaGateResponseArrayDtoItemBlockedStage
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="QaGateResponseArrayDtoItem")



@_attrs_define
class QaGateResponseArrayDtoItem:
    """ A QA gate that blocks a workflow stage on an environment until its QA config passes.

        Attributes:
            id (UUID): Stable QA-gate identifier (UUID). Gates require a passing QA verdict before a problem can advance.
            environment_id (UUID): Stable environment identifier (UUID).
            qa_config_id (UUID): Stable QA-config identifier (UUID).
            qa_config_name (str): Display name of the QA config bound to the gate.
            blocked_stage (QaGateResponseArrayDtoItemBlockedStage): Workflow stage this gate blocks until QA passes.
            min_score (float | None): Minimum normalized QA score required for the gate to pass. Null when not configured.
                Example: 0.8.
            accepted_grades (list[str]): Categorical QA grades that satisfy the gate; empty when not configured.
            created_at (str): Timestamp when the gate was created (ISO-8601, UTC).
            updated_at (str): Timestamp when the gate was last updated (ISO-8601, UTC).
     """

    id: UUID
    environment_id: UUID
    qa_config_id: UUID
    qa_config_name: str
    blocked_stage: QaGateResponseArrayDtoItemBlockedStage
    min_score: float | None
    accepted_grades: list[str]
    created_at: str
    updated_at: str





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        environment_id = str(self.environment_id)

        qa_config_id = str(self.qa_config_id)

        qa_config_name = self.qa_config_name

        blocked_stage = self.blocked_stage.value

        min_score: float | None
        min_score = self.min_score

        accepted_grades = self.accepted_grades



        created_at = self.created_at

        updated_at = self.updated_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "environmentId": environment_id,
            "qaConfigId": qa_config_id,
            "qaConfigName": qa_config_name,
            "blockedStage": blocked_stage,
            "minScore": min_score,
            "acceptedGrades": accepted_grades,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        environment_id = UUID(d.pop("environmentId"))




        qa_config_id = UUID(d.pop("qaConfigId"))




        qa_config_name = d.pop("qaConfigName")

        blocked_stage = QaGateResponseArrayDtoItemBlockedStage(d.pop("blockedStage"))




        def _parse_min_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        min_score = _parse_min_score(d.pop("minScore"))


        accepted_grades = cast(list[str], d.pop("acceptedGrades"))


        created_at = d.pop("createdAt")

        updated_at = d.pop("updatedAt")

        qa_gate_response_array_dto_item = cls(
            id=id,
            environment_id=environment_id,
            qa_config_id=qa_config_id,
            qa_config_name=qa_config_name,
            blocked_stage=blocked_stage,
            min_score=min_score,
            accepted_grades=accepted_grades,
            created_at=created_at,
            updated_at=updated_at,
        )

        return qa_gate_response_array_dto_item

