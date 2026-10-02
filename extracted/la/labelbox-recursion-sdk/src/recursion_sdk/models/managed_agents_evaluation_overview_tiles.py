from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_coverage_tile import ManagedAgentsCoverageTile
  from ..models.managed_agents_evaluation_cost import ManagedAgentsEvaluationCost
  from ..models.managed_agents_lowest_criterion import ManagedAgentsLowestCriterion
  from ..models.managed_agents_verdict_metric import ManagedAgentsVerdictMetric





T = TypeVar("T", bound="ManagedAgentsEvaluationOverviewTiles")



@_attrs_define
class ManagedAgentsEvaluationOverviewTiles:
    """ The four fixed-cardinality headline tiles for an evaluation Overview window.

        Example:
            {'coverage': {'delta_pp': 1.5, 'eligible_session_count': 1, 'evaluated_eligible_session_count': 1,
                'evaluation_snapshot_count': 1, 'history_status': 'complete', 'prior_rate': 1, 'rate': 1}, 'evaluation_cost':
                {'complete_count': 1, 'completeness': 'complete', 'delta_usd': 'example', 'evaluation_count': 1,
                'per_evaluation_usd': 'example', 'prior_per_evaluation_usd': 'example', 'total_usd': 'example'},
                'lowest_criterion': None, 'overall_pass': {'delta_pp': 1.5, 'fail_count': 1, 'not_applicable_count': 1,
                'pass_count': 1, 'prior_rate': 1, 'rate': 1}}

        Attributes:
            coverage (ManagedAgentsCoverageTile): Evaluation coverage over the immutable eligible-session cohort, with
                explicit unavailable history. Example: {'delta_pp': 1.5, 'eligible_session_count': 1,
                'evaluated_eligible_session_count': 1, 'evaluation_snapshot_count': 1, 'history_status': 'complete',
                'prior_rate': 1, 'rate': 1}.
            evaluation_cost (ManagedAgentsEvaluationCost): Exact evaluation cost totals and per-evaluation comparison
                without floating-point USD loss. Example: {'complete_count': 1, 'completeness': 'complete', 'delta_usd':
                'example', 'evaluation_count': 1, 'per_evaluation_usd': 'example', 'prior_per_evaluation_usd': 'example',
                'total_usd': 'example'}.
            lowest_criterion (ManagedAgentsLowestCriterion | None): Worst defined criterion metric, or null when none has a
                pass/fail denominator.
            overall_pass (ManagedAgentsVerdictMetric): Pass, fail, not-applicable, rate, and adjacent-window comparison for
                one verdict population. Example: {'delta_pp': 1.5, 'fail_count': 1, 'not_applicable_count': 1, 'pass_count': 1,
                'prior_rate': 1, 'rate': 1}.
     """

    coverage: ManagedAgentsCoverageTile
    evaluation_cost: ManagedAgentsEvaluationCost
    lowest_criterion: ManagedAgentsLowestCriterion | None
    overall_pass: ManagedAgentsVerdictMetric





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_coverage_tile import ManagedAgentsCoverageTile # noqa: PLC0415
        from ..models.managed_agents_evaluation_cost import ManagedAgentsEvaluationCost # noqa: PLC0415
        from ..models.managed_agents_lowest_criterion import ManagedAgentsLowestCriterion # noqa: PLC0415
        from ..models.managed_agents_verdict_metric import ManagedAgentsVerdictMetric # noqa: PLC0415
        coverage = self.coverage.to_dict()

        evaluation_cost = self.evaluation_cost.to_dict()

        lowest_criterion: dict[str, Any] | None
        if isinstance(self.lowest_criterion, ManagedAgentsLowestCriterion):
            lowest_criterion = self.lowest_criterion.to_dict()
        else:
            lowest_criterion = self.lowest_criterion

        overall_pass = self.overall_pass.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "coverage": coverage,
            "evaluation_cost": evaluation_cost,
            "lowest_criterion": lowest_criterion,
            "overall_pass": overall_pass,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_coverage_tile import ManagedAgentsCoverageTile # noqa: PLC0415
        from ..models.managed_agents_evaluation_cost import ManagedAgentsEvaluationCost # noqa: PLC0415
        from ..models.managed_agents_lowest_criterion import ManagedAgentsLowestCriterion # noqa: PLC0415
        from ..models.managed_agents_verdict_metric import ManagedAgentsVerdictMetric # noqa: PLC0415
        d = dict(src_dict)
        coverage = ManagedAgentsCoverageTile.from_dict(d.pop("coverage"))




        evaluation_cost = ManagedAgentsEvaluationCost.from_dict(d.pop("evaluation_cost"))




        def _parse_lowest_criterion(data: object) -> ManagedAgentsLowestCriterion | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                lowest_criterion_type_1 = ManagedAgentsLowestCriterion.from_dict(data)



                return lowest_criterion_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ManagedAgentsLowestCriterion | None, data)

        lowest_criterion = _parse_lowest_criterion(d.pop("lowest_criterion"))


        overall_pass = ManagedAgentsVerdictMetric.from_dict(d.pop("overall_pass"))




        managed_agents_evaluation_overview_tiles = cls(
            coverage=coverage,
            evaluation_cost=evaluation_cost,
            lowest_criterion=lowest_criterion,
            overall_pass=overall_pass,
        )

        return managed_agents_evaluation_overview_tiles

