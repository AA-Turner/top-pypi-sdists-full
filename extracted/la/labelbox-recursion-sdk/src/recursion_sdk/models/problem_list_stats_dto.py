from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.problem_list_stats_dto_analytics import ProblemListStatsDtoAnalytics
  from ..models.problem_list_stats_dto_properties_enrichment_filter_status_applied import ProblemListStatsDtoPropertiesEnrichmentFilterStatusApplied
  from ..models.problem_list_stats_dto_properties_enrichment_filter_status_degraded import ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegraded
  from ..models.problem_list_stats_dto_properties_enrichment_filter_status_not_requested import ProblemListStatsDtoPropertiesEnrichmentFilterStatusNotRequested





T = TypeVar("T", bound="ProblemListStatsDto")



@_attrs_define
class ProblemListStatsDto:
    """ Aggregate statistics for the filtered problem list on the environment-overview page.

        Example:
            {'totalProblems': 128, 'totalRuns': 512, 'totalCostUsd': 42.75, 'models': ['claude-sonnet-4-5-20250929',
                'claude-opus-4-6'], 'analytics': {'avgScoreBuckets': [{'label': '0-25%', 'count': 12, 'sampleItems': ['detect-
                surface-defects']}, {'label': '25-50%', 'count': 28, 'sampleItems': ['classify-weld-quality']}, {'label':
                '50-75%', 'count': 44, 'sampleItems': []}, {'label': '75-100%', 'count': 44, 'sampleItems': []}],
                'allScoresBuckets': [{'label': '0-25%', 'count': 48, 'sampleItems': []}, {'label': '25-50%', 'count': 112,
                'sampleItems': []}, {'label': '50-75%', 'count': 176, 'sampleItems': []}, {'label': '75-100%', 'count': 176,
                'sampleItems': []}]}, 'enrichmentFilterStatus': {'state': 'applied'}}

        Attributes:
            total_problems (int): Total number of problems that match the current filter set.
            total_runs (int): Total number of problem runs across the filtered problem set.
            total_cost_usd (float | None): Total USD spend across all runs in the filtered set. Null when no run-cost
                records exist.
            models (list[str]): Distinct sorted model names across all active runs in the environment; intentionally
                unfiltered so the Models dropdown stays stable.
            analytics (ProblemListStatsDtoAnalytics): Pre-aggregated chart buckets covering the full filtered set.
            enrichment_filter_status (ProblemListStatsDtoPropertiesEnrichmentFilterStatusApplied |
                ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegraded |
                ProblemListStatsDtoPropertiesEnrichmentFilterStatusNotRequested): Status of enrichment filtering on the server
                (applied, degraded, or not requested) for this response.
     """

    total_problems: int
    total_runs: int
    total_cost_usd: float | None
    models: list[str]
    analytics: ProblemListStatsDtoAnalytics
    enrichment_filter_status: ProblemListStatsDtoPropertiesEnrichmentFilterStatusApplied | ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegraded | ProblemListStatsDtoPropertiesEnrichmentFilterStatusNotRequested





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_list_stats_dto_analytics import ProblemListStatsDtoAnalytics # noqa: PLC0415
        from ..models.problem_list_stats_dto_properties_enrichment_filter_status_applied import ProblemListStatsDtoPropertiesEnrichmentFilterStatusApplied # noqa: PLC0415
        from ..models.problem_list_stats_dto_properties_enrichment_filter_status_degraded import ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegraded # noqa: PLC0415
        from ..models.problem_list_stats_dto_properties_enrichment_filter_status_not_requested import ProblemListStatsDtoPropertiesEnrichmentFilterStatusNotRequested # noqa: PLC0415
        total_problems = self.total_problems

        total_runs = self.total_runs

        total_cost_usd: float | None
        total_cost_usd = self.total_cost_usd

        models = self.models



        analytics = self.analytics.to_dict()

        enrichment_filter_status: dict[str, Any]
        if isinstance(self.enrichment_filter_status, ProblemListStatsDtoPropertiesEnrichmentFilterStatusNotRequested):
            enrichment_filter_status = self.enrichment_filter_status.to_dict()
        elif isinstance(self.enrichment_filter_status, ProblemListStatsDtoPropertiesEnrichmentFilterStatusApplied):
            enrichment_filter_status = self.enrichment_filter_status.to_dict()
        else:
            enrichment_filter_status = self.enrichment_filter_status.to_dict()



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "totalProblems": total_problems,
            "totalRuns": total_runs,
            "totalCostUsd": total_cost_usd,
            "models": models,
            "analytics": analytics,
            "enrichmentFilterStatus": enrichment_filter_status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_list_stats_dto_analytics import ProblemListStatsDtoAnalytics # noqa: PLC0415
        from ..models.problem_list_stats_dto_properties_enrichment_filter_status_applied import ProblemListStatsDtoPropertiesEnrichmentFilterStatusApplied # noqa: PLC0415
        from ..models.problem_list_stats_dto_properties_enrichment_filter_status_degraded import ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegraded # noqa: PLC0415
        from ..models.problem_list_stats_dto_properties_enrichment_filter_status_not_requested import ProblemListStatsDtoPropertiesEnrichmentFilterStatusNotRequested # noqa: PLC0415
        d = dict(src_dict)
        total_problems = d.pop("totalProblems")

        total_runs = d.pop("totalRuns")

        def _parse_total_cost_usd(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        total_cost_usd = _parse_total_cost_usd(d.pop("totalCostUsd"))


        models = cast(list[str], d.pop("models"))


        analytics = ProblemListStatsDtoAnalytics.from_dict(d.pop("analytics"))




        def _parse_enrichment_filter_status(data: object) -> ProblemListStatsDtoPropertiesEnrichmentFilterStatusApplied | ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegraded | ProblemListStatsDtoPropertiesEnrichmentFilterStatusNotRequested:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                enrichment_filter_status_type_0 = ProblemListStatsDtoPropertiesEnrichmentFilterStatusNotRequested.from_dict(data)



                return enrichment_filter_status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                enrichment_filter_status_type_1 = ProblemListStatsDtoPropertiesEnrichmentFilterStatusApplied.from_dict(data)



                return enrichment_filter_status_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            enrichment_filter_status_type_2 = ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegraded.from_dict(data)



            return enrichment_filter_status_type_2

        enrichment_filter_status = _parse_enrichment_filter_status(d.pop("enrichmentFilterStatus"))


        problem_list_stats_dto = cls(
            total_problems=total_problems,
            total_runs=total_runs,
            total_cost_usd=total_cost_usd,
            models=models,
            analytics=analytics,
            enrichment_filter_status=enrichment_filter_status,
        )

        return problem_list_stats_dto

