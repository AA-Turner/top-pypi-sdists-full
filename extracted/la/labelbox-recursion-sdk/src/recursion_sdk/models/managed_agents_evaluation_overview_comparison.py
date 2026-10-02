from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_overview_comparison_granularity import ManagedAgentsEvaluationOverviewComparisonGranularity
from ..models.managed_agents_evaluation_overview_comparison_metric import ManagedAgentsEvaluationOverviewComparisonMetric
from ..models.managed_agents_evaluation_overview_comparison_selection_source import ManagedAgentsEvaluationOverviewComparisonSelectionSource
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_change_marker import ManagedAgentsChangeMarker
  from ..models.managed_agents_evaluation_overview_comparison_agent import ManagedAgentsEvaluationOverviewComparisonAgent
  from ..models.managed_agents_evaluation_overview_comparison_series import ManagedAgentsEvaluationOverviewComparisonSeries





T = TypeVar("T", bound="ManagedAgentsEvaluationOverviewComparison")



@_attrs_define
class ManagedAgentsEvaluationOverviewComparison:
    """ A bounded multi-agent, immutable-version evaluation comparison over one selected metric.

        Example:
            {'agents': [{'default_target_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'display_name':
                'example-name', 'target_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'version_options': [{'created_at':
                '2026-02-18T09:30:00Z', 'has_current_observations': True, 'identity_status': 'catalog', 'is_latest': True,
                'selected': True, 'target_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'version_number': 1}],
                'version_options_truncated': True}], 'criterion_key': 'example', 'granularity': 'exact', 'markers':
                [{'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at': '2026-02-18T09:30:00Z', 'from_model':
                'example', 'kind': 'agent_version', 'target_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'to_model':
                'example', 'version_number': 1}], 'metric': 'overall', 'selection_source': 'default', 'series': [{'created_at':
                '2026-02-18T09:30:00Z', 'identity_status': 'catalog', 'is_latest': True, 'points': [{'bucket_start':
                '2026-02-18T09:30:00Z', 'fail_count': 1, 'not_applicable_count': 1, 'pass_count': 1, 'rate': 1}],
                'target_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'version_number': 1}]}

        Attributes:
            agents (list[ManagedAgentsEvaluationOverviewComparisonAgent]): Effective organization-scoped agents and their
                bounded version options.
            markers (list[ManagedAgentsChangeMarker]): Version and model-change markers for the selected trace versions.
            metric (ManagedAgentsEvaluationOverviewComparisonMetric): Whether traces aggregate overall evaluation verdicts
                or one criterion.
            selection_source (ManagedAgentsEvaluationOverviewComparisonSelectionSource): Whether the server chose the
                effective agents or the request named them explicitly.
            series (list[ManagedAgentsEvaluationOverviewComparisonSeries]): At most twelve selected agent-version traces in
                stable agent and version order.
            criterion_key (str | Unset): Selected rubric key when metric is criterion; omitted for overall.
            granularity (ManagedAgentsEvaluationOverviewComparisonGranularity | Unset): Adaptive position semantics: exact
                timestamps are trace-local, while interval granularities use shared aligned positions; omitted for the legacy
                daily response and empty adaptive collections.
     """

    agents: list[ManagedAgentsEvaluationOverviewComparisonAgent]
    markers: list[ManagedAgentsChangeMarker]
    metric: ManagedAgentsEvaluationOverviewComparisonMetric
    selection_source: ManagedAgentsEvaluationOverviewComparisonSelectionSource
    series: list[ManagedAgentsEvaluationOverviewComparisonSeries]
    criterion_key: str | Unset = UNSET
    granularity: ManagedAgentsEvaluationOverviewComparisonGranularity | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_change_marker import ManagedAgentsChangeMarker # noqa: PLC0415
        from ..models.managed_agents_evaluation_overview_comparison_agent import ManagedAgentsEvaluationOverviewComparisonAgent # noqa: PLC0415
        from ..models.managed_agents_evaluation_overview_comparison_series import ManagedAgentsEvaluationOverviewComparisonSeries # noqa: PLC0415
        agents = []
        for agents_item_data in self.agents:
            agents_item = agents_item_data.to_dict()
            agents.append(agents_item)



        markers = []
        for markers_item_data in self.markers:
            markers_item = markers_item_data.to_dict()
            markers.append(markers_item)



        metric = self.metric.value

        selection_source = self.selection_source.value

        series = []
        for series_item_data in self.series:
            series_item = series_item_data.to_dict()
            series.append(series_item)



        criterion_key = self.criterion_key

        granularity: str | Unset = UNSET
        if not isinstance(self.granularity, Unset):
            granularity = self.granularity.value



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agents": agents,
            "markers": markers,
            "metric": metric,
            "selection_source": selection_source,
            "series": series,
        })
        if criterion_key is not UNSET:
            field_dict["criterion_key"] = criterion_key
        if granularity is not UNSET:
            field_dict["granularity"] = granularity

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_change_marker import ManagedAgentsChangeMarker # noqa: PLC0415
        from ..models.managed_agents_evaluation_overview_comparison_agent import ManagedAgentsEvaluationOverviewComparisonAgent # noqa: PLC0415
        from ..models.managed_agents_evaluation_overview_comparison_series import ManagedAgentsEvaluationOverviewComparisonSeries # noqa: PLC0415
        d = dict(src_dict)
        agents = []
        _agents = d.pop("agents")
        for agents_item_data in (_agents):
            agents_item = ManagedAgentsEvaluationOverviewComparisonAgent.from_dict(agents_item_data)



            agents.append(agents_item)


        markers = []
        _markers = d.pop("markers")
        for markers_item_data in (_markers):
            markers_item = ManagedAgentsChangeMarker.from_dict(markers_item_data)



            markers.append(markers_item)


        metric = ManagedAgentsEvaluationOverviewComparisonMetric(d.pop("metric"))




        selection_source = ManagedAgentsEvaluationOverviewComparisonSelectionSource(d.pop("selection_source"))




        series = []
        _series = d.pop("series")
        for series_item_data in (_series):
            series_item = ManagedAgentsEvaluationOverviewComparisonSeries.from_dict(series_item_data)



            series.append(series_item)


        criterion_key = d.pop("criterion_key", UNSET)

        _granularity = d.pop("granularity", UNSET)
        granularity: ManagedAgentsEvaluationOverviewComparisonGranularity | Unset
        if isinstance(_granularity,  Unset):
            granularity = UNSET
        else:
            granularity = ManagedAgentsEvaluationOverviewComparisonGranularity(_granularity)




        managed_agents_evaluation_overview_comparison = cls(
            agents=agents,
            markers=markers,
            metric=metric,
            selection_source=selection_source,
            series=series,
            criterion_key=criterion_key,
            granularity=granularity,
        )

        return managed_agents_evaluation_overview_comparison

