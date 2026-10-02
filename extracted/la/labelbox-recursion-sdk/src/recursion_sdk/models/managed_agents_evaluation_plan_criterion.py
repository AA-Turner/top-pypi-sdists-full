from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsEvaluationPlanCriterion")



@_attrs_define
class ManagedAgentsEvaluationPlanCriterion:
    """ One stable rubric criterion frozen from the evaluator version for the complete run.

        Example:
            {'criterion_key': 'example', 'criterion_text': 'example'}

        Attributes:
            criterion_key (str): Stable rubric key used to join verdicts across the run.
            criterion_text (str): Frozen rubric instruction evaluated for every target.
     """

    criterion_key: str
    criterion_text: str





    def to_dict(self) -> dict[str, Any]:
        criterion_key = self.criterion_key

        criterion_text = self.criterion_text


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "criterion_key": criterion_key,
            "criterion_text": criterion_text,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        criterion_key = d.pop("criterion_key")

        criterion_text = d.pop("criterion_text")

        managed_agents_evaluation_plan_criterion = cls(
            criterion_key=criterion_key,
            criterion_text=criterion_text,
        )

        return managed_agents_evaluation_plan_criterion

