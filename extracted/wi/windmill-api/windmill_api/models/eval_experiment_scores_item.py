from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.eval_experiment_scores_item_kind import EvalExperimentScoresItemKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="EvalExperimentScoresItem")


@_attrs_define
class EvalExperimentScoresItem:
    """One scorer's headline for one run: the two numbers a column reports, over that run's cells.

    Attributes:
        scorer_id (str):
        name (str): What the column is called in the dataset that ran it, resolved server-side because a list of runs
            spanning datasets cannot hold every dataset's scorers to look it up.
        kind (EvalExperimentScoresItemKind):
        scored (int):
        failed (int): How many of the run's cells the column failed on. A column that failed on all of them has no
            number to report and is still one of the columns that ran.
        mean (Union[Unset, float]):
        pass_rate (Union[Unset, float]): The share of scored cells at or above the column's threshold, for a column that
            has one. Absent where the column has no threshold and the mean is the whole headline.
    """

    scorer_id: str
    name: str
    kind: EvalExperimentScoresItemKind
    scored: int
    failed: int
    mean: Union[Unset, float] = UNSET
    pass_rate: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scorer_id = self.scorer_id
        name = self.name
        kind = self.kind.value

        scored = self.scored
        failed = self.failed
        mean = self.mean
        pass_rate = self.pass_rate

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scorer_id": scorer_id,
                "name": name,
                "kind": kind,
                "scored": scored,
                "failed": failed,
            }
        )
        if mean is not UNSET:
            field_dict["mean"] = mean
        if pass_rate is not UNSET:
            field_dict["pass_rate"] = pass_rate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        scorer_id = d.pop("scorer_id")

        name = d.pop("name")

        kind = EvalExperimentScoresItemKind(d.pop("kind"))

        scored = d.pop("scored")

        failed = d.pop("failed")

        mean = d.pop("mean", UNSET)

        pass_rate = d.pop("pass_rate", UNSET)

        eval_experiment_scores_item = cls(
            scorer_id=scorer_id,
            name=name,
            kind=kind,
            scored=scored,
            failed=failed,
            mean=mean,
            pass_rate=pass_rate,
        )

        eval_experiment_scores_item.additional_properties = d
        return eval_experiment_scores_item

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
