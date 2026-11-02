from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExperimentResultsResponse200RowsItemScoresItem")


@_attrs_define
class ExperimentResultsResponse200RowsItemScoresItem:
    """One scorer's verdict on one run, and how it compares with the baseline.

    Attributes:
        scorer_id (str):
        pending (bool): A scoring job is still running for this cell.
        definition_changed (bool): The baseline's score came from a different definition of this scorer, so the delta is
            a change of scorer as much as a change of agent.
        score (Union[Unset, float]):
        reason (Union[Unset, str]):
        checks (Union[Unset, Any]):
        error (Union[Unset, str]):
        not_applicable (Union[Unset, bool]): The scorer read this case and had nothing to measure on it. Left out of the
            column's mean and pass rate rather than counted as a zero.
        passed (Union[Unset, bool]): Which side of the scorer's `pass_if` threshold the score fell on. Absent when the
            column has no threshold, or has no score yet.
        baseline (Union[Unset, float]): The same scorer's number on the baseline experiment.
    """

    scorer_id: str
    pending: bool
    definition_changed: bool
    score: Union[Unset, float] = UNSET
    reason: Union[Unset, str] = UNSET
    checks: Union[Unset, Any] = UNSET
    error: Union[Unset, str] = UNSET
    not_applicable: Union[Unset, bool] = UNSET
    passed: Union[Unset, bool] = UNSET
    baseline: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scorer_id = self.scorer_id
        pending = self.pending
        definition_changed = self.definition_changed
        score = self.score
        reason = self.reason
        checks = self.checks
        error = self.error
        not_applicable = self.not_applicable
        passed = self.passed
        baseline = self.baseline

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scorer_id": scorer_id,
                "pending": pending,
                "definition_changed": definition_changed,
            }
        )
        if score is not UNSET:
            field_dict["score"] = score
        if reason is not UNSET:
            field_dict["reason"] = reason
        if checks is not UNSET:
            field_dict["checks"] = checks
        if error is not UNSET:
            field_dict["error"] = error
        if not_applicable is not UNSET:
            field_dict["not_applicable"] = not_applicable
        if passed is not UNSET:
            field_dict["passed"] = passed
        if baseline is not UNSET:
            field_dict["baseline"] = baseline

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        scorer_id = d.pop("scorer_id")

        pending = d.pop("pending")

        definition_changed = d.pop("definition_changed")

        score = d.pop("score", UNSET)

        reason = d.pop("reason", UNSET)

        checks = d.pop("checks", UNSET)

        error = d.pop("error", UNSET)

        not_applicable = d.pop("not_applicable", UNSET)

        passed = d.pop("passed", UNSET)

        baseline = d.pop("baseline", UNSET)

        experiment_results_response_200_rows_item_scores_item = cls(
            scorer_id=scorer_id,
            pending=pending,
            definition_changed=definition_changed,
            score=score,
            reason=reason,
            checks=checks,
            error=error,
            not_applicable=not_applicable,
            passed=passed,
            baseline=baseline,
        )

        experiment_results_response_200_rows_item_scores_item.additional_properties = d
        return experiment_results_response_200_rows_item_scores_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
