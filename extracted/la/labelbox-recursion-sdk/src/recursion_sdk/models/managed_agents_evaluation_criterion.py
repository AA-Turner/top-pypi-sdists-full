from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_criterion_verdict import ManagedAgentsEvaluationCriterionVerdict
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsEvaluationCriterion")



@_attrs_define
class ManagedAgentsEvaluationCriterion:
    """ One immutable rubric-criterion verdict with rationale and transcript evidence references.

        Example:
            {'criterion_key': 'example', 'evidence_event_ids': ['9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'], 'rationale':
                'example', 'verdict': 'pass'}

        Attributes:
            criterion_key (str): Stable rubric key identifying this criterion.
            evidence_event_ids (list[UUID]): Ordered target event IDs cited as evidence, all at or before the snapshot.
            rationale (str): Evaluator explanation supporting the criterion verdict.
            verdict (ManagedAgentsEvaluationCriterionVerdict): Immutable verdict for this rubric criterion.
     """

    criterion_key: str
    evidence_event_ids: list[UUID]
    rationale: str
    verdict: ManagedAgentsEvaluationCriterionVerdict





    def to_dict(self) -> dict[str, Any]:
        criterion_key = self.criterion_key

        evidence_event_ids = []
        for evidence_event_ids_item_data in self.evidence_event_ids:
            evidence_event_ids_item = str(evidence_event_ids_item_data)
            evidence_event_ids.append(evidence_event_ids_item)



        rationale = self.rationale

        verdict = self.verdict.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "criterion_key": criterion_key,
            "evidence_event_ids": evidence_event_ids,
            "rationale": rationale,
            "verdict": verdict,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        criterion_key = d.pop("criterion_key")

        evidence_event_ids = []
        _evidence_event_ids = d.pop("evidence_event_ids")
        for evidence_event_ids_item_data in (_evidence_event_ids):
            evidence_event_ids_item = UUID(evidence_event_ids_item_data)



            evidence_event_ids.append(evidence_event_ids_item)


        rationale = d.pop("rationale")

        verdict = ManagedAgentsEvaluationCriterionVerdict(d.pop("verdict"))




        managed_agents_evaluation_criterion = cls(
            criterion_key=criterion_key,
            evidence_event_ids=evidence_event_ids,
            rationale=rationale,
            verdict=verdict,
        )

        return managed_agents_evaluation_criterion

