from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScorerMean")


@_attrs_define
class ScorerMean:
    """A column's summary. There is no single number for a dataset: averaging a judge with an exact match would invent one.

    Attributes:
        scorer_id (str):
        scored (int):
        missing_in_baseline (int): Cells the baseline has no score for, so a column the baseline never ran shows as
            unscored rather than as a spurious difference.
        definition_changed (bool):
        mean (Union[Unset, float]):
        baseline_mean (Union[Unset, float]):
        pass_rate (Union[Unset, float]): The share of scored cells that passed, for a column with a threshold. Reported
            beside the mean rather than instead of it: a pass rate says how many cases are good enough, a mean says by how
            much, and neither answers the other's question.
        baseline_pass_rate (Union[Unset, float]):
    """

    scorer_id: str
    scored: int
    missing_in_baseline: int
    definition_changed: bool
    mean: Union[Unset, float] = UNSET
    baseline_mean: Union[Unset, float] = UNSET
    pass_rate: Union[Unset, float] = UNSET
    baseline_pass_rate: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scorer_id = self.scorer_id
        scored = self.scored
        missing_in_baseline = self.missing_in_baseline
        definition_changed = self.definition_changed
        mean = self.mean
        baseline_mean = self.baseline_mean
        pass_rate = self.pass_rate
        baseline_pass_rate = self.baseline_pass_rate

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scorer_id": scorer_id,
                "scored": scored,
                "missing_in_baseline": missing_in_baseline,
                "definition_changed": definition_changed,
            }
        )
        if mean is not UNSET:
            field_dict["mean"] = mean
        if baseline_mean is not UNSET:
            field_dict["baseline_mean"] = baseline_mean
        if pass_rate is not UNSET:
            field_dict["pass_rate"] = pass_rate
        if baseline_pass_rate is not UNSET:
            field_dict["baseline_pass_rate"] = baseline_pass_rate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        scorer_id = d.pop("scorer_id")

        scored = d.pop("scored")

        missing_in_baseline = d.pop("missing_in_baseline")

        definition_changed = d.pop("definition_changed")

        mean = d.pop("mean", UNSET)

        baseline_mean = d.pop("baseline_mean", UNSET)

        pass_rate = d.pop("pass_rate", UNSET)

        baseline_pass_rate = d.pop("baseline_pass_rate", UNSET)

        scorer_mean = cls(
            scorer_id=scorer_id,
            scored=scored,
            missing_in_baseline=missing_in_baseline,
            definition_changed=definition_changed,
            mean=mean,
            baseline_mean=baseline_mean,
            pass_rate=pass_rate,
            baseline_pass_rate=baseline_pass_rate,
        )

        scorer_mean.additional_properties = d
        return scorer_mean

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
