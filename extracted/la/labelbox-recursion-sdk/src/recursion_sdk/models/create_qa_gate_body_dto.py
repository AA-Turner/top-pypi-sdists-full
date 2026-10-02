from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_qa_gate_body_dto_blocked_stage import CreateQaGateBodyDtoBlockedStage
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="CreateQaGateBodyDto")



@_attrs_define
class CreateQaGateBodyDto:
    """ Request body for creating a QA gate that blocks a workflow stage until QA passes.

        Example:
            {'qaConfigId': 'd6bcc57c-7b71-4369-98da-ab69d9571bb9', 'blockedStage': 'submitting', 'minScore': 0.8,
                'acceptedGrades': ['pass']}

        Attributes:
            qa_config_id (UUID): Stable QA-config identifier (UUID).
            blocked_stage (CreateQaGateBodyDtoBlockedStage | Unset): Workflow stage this gate will block until QA passes.
                Default: CreateQaGateBodyDtoBlockedStage.SUBMITTING.
            min_score (float | Unset): Minimum normalized QA score in [0, 1] required for the gate to pass. At least one of
                minimum score or accepted grades must be provided. Example: 0.8.
            accepted_grades (list[str] | Unset): Set of categorical QA grades that satisfy the gate. At least one of minimum
                score or accepted grades must be provided.
     """

    qa_config_id: UUID
    blocked_stage: CreateQaGateBodyDtoBlockedStage | Unset = CreateQaGateBodyDtoBlockedStage.SUBMITTING
    min_score: float | Unset = UNSET
    accepted_grades: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        qa_config_id = str(self.qa_config_id)

        blocked_stage: str | Unset = UNSET
        if not isinstance(self.blocked_stage, Unset):
            blocked_stage = self.blocked_stage.value


        min_score = self.min_score

        accepted_grades: list[str] | Unset = UNSET
        if not isinstance(self.accepted_grades, Unset):
            accepted_grades = self.accepted_grades




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "qaConfigId": qa_config_id,
        })
        if blocked_stage is not UNSET:
            field_dict["blockedStage"] = blocked_stage
        if min_score is not UNSET:
            field_dict["minScore"] = min_score
        if accepted_grades is not UNSET:
            field_dict["acceptedGrades"] = accepted_grades

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        qa_config_id = UUID(d.pop("qaConfigId"))




        _blocked_stage = d.pop("blockedStage", UNSET)
        blocked_stage: CreateQaGateBodyDtoBlockedStage | Unset
        if isinstance(_blocked_stage,  Unset):
            blocked_stage = UNSET
        else:
            blocked_stage = CreateQaGateBodyDtoBlockedStage(_blocked_stage)




        min_score = d.pop("minScore", UNSET)

        accepted_grades = cast(list[str], d.pop("acceptedGrades", UNSET))


        create_qa_gate_body_dto = cls(
            qa_config_id=qa_config_id,
            blocked_stage=blocked_stage,
            min_score=min_score,
            accepted_grades=accepted_grades,
        )


        create_qa_gate_body_dto.additional_properties = d
        return create_qa_gate_body_dto

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
