from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsOutcomeCriterion")



@_attrs_define
class ManagedAgentsOutcomeCriterion:
    """ One scored line of a rubric: the criterion, the grader's verdict on it, and the events cited as evidence. Read these
    to see why an outcome passed or failed rather than only that it did.

        Example:
            {'criterion_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'criterion_text': 'example', 'evidence_event_ids':
                ['example'], 'rationale': 'example', 'section': 'example', 'verdict': 'example', 'weight': 1.5}

        Attributes:
            criterion_id (str): Identifies a criterion as its rubric's digest plus its ordinal, so the same rubric reused
                across sessions scores comparable criteria. Any edit to the rubric changes every id in it.
            criterion_text (str): The rubric line this verdict scores, as written in the rubric.
            verdict (str): Grader's judgment on this criterion, conventionally pass, fail, or not_applicable when the
                criterion did not apply to this run. Not a closed set: the value is recorded as the grader wrote it.
            weight (float): Relative importance the rubric gives this criterion when aggregating a score.
            evidence_event_ids (list[str] | Unset): Session events (UUIDs) the grader cites as justification, so a reviewer
                can check the verdict against the transcript instead of trusting it.
            rationale (str | Unset): Grader's reasoning for the verdict on this criterion.
            section (str | Unset): Rubric heading this criterion sits under, when the rubric is organized into sections.
     """

    criterion_id: str
    criterion_text: str
    verdict: str
    weight: float
    evidence_event_ids: list[str] | Unset = UNSET
    rationale: str | Unset = UNSET
    section: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        criterion_id = self.criterion_id

        criterion_text = self.criterion_text

        verdict = self.verdict

        weight = self.weight

        evidence_event_ids: list[str] | Unset = UNSET
        if not isinstance(self.evidence_event_ids, Unset):
            evidence_event_ids = self.evidence_event_ids



        rationale = self.rationale

        section = self.section


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "criterion_id": criterion_id,
            "criterion_text": criterion_text,
            "verdict": verdict,
            "weight": weight,
        })
        if evidence_event_ids is not UNSET:
            field_dict["evidence_event_ids"] = evidence_event_ids
        if rationale is not UNSET:
            field_dict["rationale"] = rationale
        if section is not UNSET:
            field_dict["section"] = section

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        criterion_id = d.pop("criterion_id")

        criterion_text = d.pop("criterion_text")

        verdict = d.pop("verdict")

        weight = d.pop("weight")

        evidence_event_ids = cast(list[str], d.pop("evidence_event_ids", UNSET))


        rationale = d.pop("rationale", UNSET)

        section = d.pop("section", UNSET)

        managed_agents_outcome_criterion = cls(
            criterion_id=criterion_id,
            criterion_text=criterion_text,
            verdict=verdict,
            weight=weight,
            evidence_event_ids=evidence_event_ids,
            rationale=rationale,
            section=section,
        )


        managed_agents_outcome_criterion.additional_properties = d
        return managed_agents_outcome_criterion

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
