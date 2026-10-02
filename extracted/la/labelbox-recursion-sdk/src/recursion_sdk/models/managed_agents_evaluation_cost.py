from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_cost_completeness_type_1 import ManagedAgentsEvaluationCostCompletenessType1
from ..models.managed_agents_evaluation_cost_completeness_type_2_type_1 import ManagedAgentsEvaluationCostCompletenessType2Type1
from ..models.managed_agents_evaluation_cost_completeness_type_3_type_1 import ManagedAgentsEvaluationCostCompletenessType3Type1
from typing import cast






T = TypeVar("T", bound="ManagedAgentsEvaluationCost")



@_attrs_define
class ManagedAgentsEvaluationCost:
    """ Exact evaluation cost totals and per-evaluation comparison without floating-point USD loss.

        Example:
            {'complete_count': 1, 'completeness': 'complete', 'delta_usd': 'example', 'evaluation_count': 1,
                'per_evaluation_usd': 'example', 'prior_per_evaluation_usd': 'example', 'total_usd': 'example'}

        Attributes:
            complete_count (int): Evaluations whose complete priced cost contributes to the total.
            completeness (ManagedAgentsEvaluationCostCompletenessType1 | ManagedAgentsEvaluationCostCompletenessType2Type1 |
                ManagedAgentsEvaluationCostCompletenessType3Type1 | None): Aggregate cost-finality state, or null when the
                window has no evaluations.
            delta_usd (None | str): Exact current minus prior per-evaluation USD, or null when either side is undefined.
            evaluation_count (int): Immutable evaluations included in the current cost population.
            per_evaluation_usd (None | str): Exact current-window USD total per cost-complete evaluation, or null when
                undefined.
            prior_per_evaluation_usd (None | str): Equivalent exact per-evaluation USD for the adjacent prior window, or
                null when undefined.
            total_usd (None | str): Exact decimal USD total, or null when no complete priced total exists.
     """

    complete_count: int
    completeness: ManagedAgentsEvaluationCostCompletenessType1 | ManagedAgentsEvaluationCostCompletenessType2Type1 | ManagedAgentsEvaluationCostCompletenessType3Type1 | None
    delta_usd: None | str
    evaluation_count: int
    per_evaluation_usd: None | str
    prior_per_evaluation_usd: None | str
    total_usd: None | str





    def to_dict(self) -> dict[str, Any]:
        complete_count = self.complete_count

        completeness: None | str
        if isinstance(self.completeness, ManagedAgentsEvaluationCostCompletenessType1):
            completeness = self.completeness.value
        elif isinstance(self.completeness, ManagedAgentsEvaluationCostCompletenessType2Type1):
            completeness = self.completeness.value
        elif isinstance(self.completeness, ManagedAgentsEvaluationCostCompletenessType3Type1):
            completeness = self.completeness.value
        else:
            completeness = self.completeness

        delta_usd: None | str
        delta_usd = self.delta_usd

        evaluation_count = self.evaluation_count

        per_evaluation_usd: None | str
        per_evaluation_usd = self.per_evaluation_usd

        prior_per_evaluation_usd: None | str
        prior_per_evaluation_usd = self.prior_per_evaluation_usd

        total_usd: None | str
        total_usd = self.total_usd


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "complete_count": complete_count,
            "completeness": completeness,
            "delta_usd": delta_usd,
            "evaluation_count": evaluation_count,
            "per_evaluation_usd": per_evaluation_usd,
            "prior_per_evaluation_usd": prior_per_evaluation_usd,
            "total_usd": total_usd,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        complete_count = d.pop("complete_count")

        def _parse_completeness(data: object) -> ManagedAgentsEvaluationCostCompletenessType1 | ManagedAgentsEvaluationCostCompletenessType2Type1 | ManagedAgentsEvaluationCostCompletenessType3Type1 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completeness_type_1 = ManagedAgentsEvaluationCostCompletenessType1(data)



                return completeness_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completeness_type_2_type_1 = ManagedAgentsEvaluationCostCompletenessType2Type1(data)



                return completeness_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completeness_type_3_type_1 = ManagedAgentsEvaluationCostCompletenessType3Type1(data)



                return completeness_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ManagedAgentsEvaluationCostCompletenessType1 | ManagedAgentsEvaluationCostCompletenessType2Type1 | ManagedAgentsEvaluationCostCompletenessType3Type1 | None, data)

        completeness = _parse_completeness(d.pop("completeness"))


        def _parse_delta_usd(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        delta_usd = _parse_delta_usd(d.pop("delta_usd"))


        evaluation_count = d.pop("evaluation_count")

        def _parse_per_evaluation_usd(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        per_evaluation_usd = _parse_per_evaluation_usd(d.pop("per_evaluation_usd"))


        def _parse_prior_per_evaluation_usd(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        prior_per_evaluation_usd = _parse_prior_per_evaluation_usd(d.pop("prior_per_evaluation_usd"))


        def _parse_total_usd(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        total_usd = _parse_total_usd(d.pop("total_usd"))


        managed_agents_evaluation_cost = cls(
            complete_count=complete_count,
            completeness=completeness,
            delta_usd=delta_usd,
            evaluation_count=evaluation_count,
            per_evaluation_usd=per_evaluation_usd,
            prior_per_evaluation_usd=prior_per_evaluation_usd,
            total_usd=total_usd,
        )

        return managed_agents_evaluation_cost

