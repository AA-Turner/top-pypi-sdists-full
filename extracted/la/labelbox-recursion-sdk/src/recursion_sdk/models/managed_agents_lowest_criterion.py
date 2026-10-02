from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_verdict_metric import ManagedAgentsVerdictMetric





T = TypeVar("T", bound="ManagedAgentsLowestCriterion")



@_attrs_define
class ManagedAgentsLowestCriterion:
    """ The rubric criterion with the lowest defined pass rate in the current window.

        Example:
            {'criterion_key': 'example', 'metric': {'delta_pp': 1.5, 'fail_count': 1, 'not_applicable_count': 1,
                'pass_count': 1, 'prior_rate': 1, 'rate': 1}}

        Attributes:
            criterion_key (str): Rubric key with the lowest defined current-window pass rate.
            metric (ManagedAgentsVerdictMetric): Pass, fail, not-applicable, rate, and adjacent-window comparison for one
                verdict population. Example: {'delta_pp': 1.5, 'fail_count': 1, 'not_applicable_count': 1, 'pass_count': 1,
                'prior_rate': 1, 'rate': 1}.
     """

    criterion_key: str
    metric: ManagedAgentsVerdictMetric





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_verdict_metric import ManagedAgentsVerdictMetric # noqa: PLC0415
        criterion_key = self.criterion_key

        metric = self.metric.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "criterion_key": criterion_key,
            "metric": metric,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_verdict_metric import ManagedAgentsVerdictMetric # noqa: PLC0415
        d = dict(src_dict)
        criterion_key = d.pop("criterion_key")

        metric = ManagedAgentsVerdictMetric.from_dict(d.pop("metric"))




        managed_agents_lowest_criterion = cls(
            criterion_key=criterion_key,
            metric=metric,
        )

        return managed_agents_lowest_criterion

