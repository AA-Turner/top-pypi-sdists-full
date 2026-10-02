from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_overview_response_change_markers_status import ManagedAgentsEvaluationOverviewResponseChangeMarkersStatus
from ..models.managed_agents_evaluation_overview_response_criterion_series_granularity import ManagedAgentsEvaluationOverviewResponseCriterionSeriesGranularity
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_agent_row import ManagedAgentsAgentRow
  from ..models.managed_agents_change_marker import ManagedAgentsChangeMarker
  from ..models.managed_agents_criterion_series_point import ManagedAgentsCriterionSeriesPoint
  from ..models.managed_agents_evaluation_overview_comparison import ManagedAgentsEvaluationOverviewComparison
  from ..models.managed_agents_evaluation_overview_tiles import ManagedAgentsEvaluationOverviewTiles





T = TypeVar("T", bound="ManagedAgentsEvaluationOverviewResponse")



@_attrs_define
class ManagedAgentsEvaluationOverviewResponse:
    """ Complete fixed-window evaluation Overview plus an optional signed target-agent continuation.

        Example:
            {'agent_rows': [{'criterion_metrics': [None], 'evaluation_count': 1, 'newest_failures': [{'created_at':
                '2026-02-18T09:30:00Z', 'evaluation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'failed_criterion_keys':
                ['example'], 'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_available': True,
                'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'overall_pass': {'delta_pp': 1.5, 'fail_count':
                1, 'not_applicable_count': 1, 'pass_count': 1, 'prior_rate': 1, 'rate': 1}, 'target_agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'as_of': '2026-02-18T09:30:00Z', 'change_markers':
                [{'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at': '2026-02-18T09:30:00Z', 'from_model':
                'example', 'kind': 'agent_version', 'target_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'to_model':
                'example', 'version_number': 1}], 'change_markers_status': 'complete', 'comparison': {'agents':
                [{'default_target_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'display_name': 'example-name',
                'target_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'version_options': [{'created_at':
                '2026-02-18T09:30:00Z', 'has_current_observations': True, 'identity_status': 'catalog', 'is_latest': True,
                'selected': True, 'target_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'version_number': 1}],
                'version_options_truncated': True}], 'criterion_key': 'example', 'granularity': 'exact', 'markers':
                [{'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at': '2026-02-18T09:30:00Z', 'from_model':
                'example', 'kind': 'agent_version', 'target_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'to_model':
                'example', 'version_number': 1}], 'metric': 'overall', 'selection_source': 'default', 'series': [{'created_at':
                '2026-02-18T09:30:00Z', 'identity_status': 'catalog', 'is_latest': True, 'points': [{'bucket_start':
                '2026-02-18T09:30:00Z', 'fail_count': 1, 'not_applicable_count': 1, 'pass_count': 1, 'rate': 1}],
                'target_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'version_number': 1}]}, 'criterion_columns': ['example'],
                'criterion_series': [{'bucket_start': '2026-02-18T09:30:00Z', 'criterion_key': 'example', 'fail_count': 1,
                'not_applicable_count': 1, 'pass_count': 1, 'rate': 1}], 'criterion_series_granularity': 'exact', 'from':
                '2026-02-18T09:30:00Z', 'next_page_token': 'example', 'prior_from': '2026-02-18T09:30:00Z', 'prior_to':
                '2026-02-18T09:30:00Z', 'tiles': {'coverage': {'delta_pp': 1.5, 'eligible_session_count': 1,
                'evaluated_eligible_session_count': 1, 'evaluation_snapshot_count': 1, 'history_status': 'complete',
                'prior_rate': 1, 'rate': 1}, 'evaluation_cost': {'complete_count': 1, 'completeness': 'complete', 'delta_usd':
                'example', 'evaluation_count': 1, 'per_evaluation_usd': 'example', 'prior_per_evaluation_usd': 'example',
                'total_usd': 'example'}, 'lowest_criterion': None, 'overall_pass': {'delta_pp': 1.5, 'fail_count': 1,
                'not_applicable_count': 1, 'pass_count': 1, 'prior_rate': 1, 'rate': 1}}, 'to': '2026-02-18T09:30:00Z'}

        Attributes:
            agent_rows (list[ManagedAgentsAgentRow]): Ranked target-agent metric rows for this signed cursor page.
            as_of (datetime.datetime): Durable analytics watermark freezing every query in this response.
            change_markers (list[ManagedAgentsChangeMarker]): Immutable agent-version and model markers when one target
                agent is selected.
            change_markers_status (ManagedAgentsEvaluationOverviewResponseChangeMarkersStatus): Whether markers are complete
                or require selecting one target agent.
            comparison (ManagedAgentsEvaluationOverviewComparison): A bounded multi-agent, immutable-version evaluation
                comparison over one selected metric. Example: {'agents': [{'default_target_agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'display_name': 'example-name', 'target_agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'version_options': [{'created_at': '2026-02-18T09:30:00Z',
                'has_current_observations': True, 'identity_status': 'catalog', 'is_latest': True, 'selected': True,
                'target_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'version_number': 1}],
                'version_options_truncated': True}], 'criterion_key': 'example', 'granularity': 'exact', 'markers':
                [{'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at': '2026-02-18T09:30:00Z', 'from_model':
                'example', 'kind': 'agent_version', 'target_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'to_model':
                'example', 'version_number': 1}], 'metric': 'overall', 'selection_source': 'default', 'series': [{'created_at':
                '2026-02-18T09:30:00Z', 'identity_status': 'catalog', 'is_latest': True, 'points': [{'bucket_start':
                '2026-02-18T09:30:00Z', 'fail_count': 1, 'not_applicable_count': 1, 'pass_count': 1, 'rate': 1}],
                'target_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'version_number': 1}]}.
            criterion_columns (list[str]): Stable key order used to align every agent row's criterion_metrics array.
            criterion_series (list[ManagedAgentsCriterionSeriesPoint]): Aligned criterion verdict series for the complete
                frozen window; legacy responses use a daily grid.
            from_ (datetime.datetime): Inclusive UTC start of the current Overview window.
            prior_from (datetime.datetime): Inclusive UTC start of the adjacent equal-length prior window.
            prior_to (datetime.datetime): Exclusive UTC end of the prior window, equal to from.
            tiles (ManagedAgentsEvaluationOverviewTiles): The four fixed-cardinality headline tiles for an evaluation
                Overview window. Example: {'coverage': {'delta_pp': 1.5, 'eligible_session_count': 1,
                'evaluated_eligible_session_count': 1, 'evaluation_snapshot_count': 1, 'history_status': 'complete',
                'prior_rate': 1, 'rate': 1}, 'evaluation_cost': {'complete_count': 1, 'completeness': 'complete', 'delta_usd':
                'example', 'evaluation_count': 1, 'per_evaluation_usd': 'example', 'prior_per_evaluation_usd': 'example',
                'total_usd': 'example'}, 'lowest_criterion': None, 'overall_pass': {'delta_pp': 1.5, 'fail_count': 1,
                'not_applicable_count': 1, 'pass_count': 1, 'prior_rate': 1, 'rate': 1}}.
            to (datetime.datetime): Exclusive UTC end of the current window, equal to as_of.
            criterion_series_granularity (ManagedAgentsEvaluationOverviewResponseCriterionSeriesGranularity | Unset):
                Adaptive position semantics: exact timestamps are criterion-local, while interval granularities use shared
                aligned positions; omitted for the legacy daily response and empty adaptive collections.
            next_page_token (str | Unset): Signed one-hour continuation for the next ranked target-agent page at the same
                watermark.
     """

    agent_rows: list[ManagedAgentsAgentRow]
    as_of: datetime.datetime
    change_markers: list[ManagedAgentsChangeMarker]
    change_markers_status: ManagedAgentsEvaluationOverviewResponseChangeMarkersStatus
    comparison: ManagedAgentsEvaluationOverviewComparison
    criterion_columns: list[str]
    criterion_series: list[ManagedAgentsCriterionSeriesPoint]
    from_: datetime.datetime
    prior_from: datetime.datetime
    prior_to: datetime.datetime
    tiles: ManagedAgentsEvaluationOverviewTiles
    to: datetime.datetime
    criterion_series_granularity: ManagedAgentsEvaluationOverviewResponseCriterionSeriesGranularity | Unset = UNSET
    next_page_token: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_agent_row import ManagedAgentsAgentRow # noqa: PLC0415
        from ..models.managed_agents_change_marker import ManagedAgentsChangeMarker # noqa: PLC0415
        from ..models.managed_agents_criterion_series_point import ManagedAgentsCriterionSeriesPoint # noqa: PLC0415
        from ..models.managed_agents_evaluation_overview_comparison import ManagedAgentsEvaluationOverviewComparison # noqa: PLC0415
        from ..models.managed_agents_evaluation_overview_tiles import ManagedAgentsEvaluationOverviewTiles # noqa: PLC0415
        agent_rows = []
        for agent_rows_item_data in self.agent_rows:
            agent_rows_item = agent_rows_item_data.to_dict()
            agent_rows.append(agent_rows_item)



        as_of = self.as_of.isoformat()

        change_markers = []
        for change_markers_item_data in self.change_markers:
            change_markers_item = change_markers_item_data.to_dict()
            change_markers.append(change_markers_item)



        change_markers_status = self.change_markers_status.value

        comparison = self.comparison.to_dict()

        criterion_columns = self.criterion_columns



        criterion_series = []
        for criterion_series_item_data in self.criterion_series:
            criterion_series_item = criterion_series_item_data.to_dict()
            criterion_series.append(criterion_series_item)



        from_ = self.from_.isoformat()

        prior_from = self.prior_from.isoformat()

        prior_to = self.prior_to.isoformat()

        tiles = self.tiles.to_dict()

        to = self.to.isoformat()

        criterion_series_granularity: str | Unset = UNSET
        if not isinstance(self.criterion_series_granularity, Unset):
            criterion_series_granularity = self.criterion_series_granularity.value


        next_page_token = self.next_page_token


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_rows": agent_rows,
            "as_of": as_of,
            "change_markers": change_markers,
            "change_markers_status": change_markers_status,
            "comparison": comparison,
            "criterion_columns": criterion_columns,
            "criterion_series": criterion_series,
            "from": from_,
            "prior_from": prior_from,
            "prior_to": prior_to,
            "tiles": tiles,
            "to": to,
        })
        if criterion_series_granularity is not UNSET:
            field_dict["criterion_series_granularity"] = criterion_series_granularity
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_agent_row import ManagedAgentsAgentRow # noqa: PLC0415
        from ..models.managed_agents_change_marker import ManagedAgentsChangeMarker # noqa: PLC0415
        from ..models.managed_agents_criterion_series_point import ManagedAgentsCriterionSeriesPoint # noqa: PLC0415
        from ..models.managed_agents_evaluation_overview_comparison import ManagedAgentsEvaluationOverviewComparison # noqa: PLC0415
        from ..models.managed_agents_evaluation_overview_tiles import ManagedAgentsEvaluationOverviewTiles # noqa: PLC0415
        d = dict(src_dict)
        agent_rows = []
        _agent_rows = d.pop("agent_rows")
        for agent_rows_item_data in (_agent_rows):
            agent_rows_item = ManagedAgentsAgentRow.from_dict(agent_rows_item_data)



            agent_rows.append(agent_rows_item)


        as_of = datetime.datetime.fromisoformat(d.pop("as_of"))




        change_markers = []
        _change_markers = d.pop("change_markers")
        for change_markers_item_data in (_change_markers):
            change_markers_item = ManagedAgentsChangeMarker.from_dict(change_markers_item_data)



            change_markers.append(change_markers_item)


        change_markers_status = ManagedAgentsEvaluationOverviewResponseChangeMarkersStatus(d.pop("change_markers_status"))




        comparison = ManagedAgentsEvaluationOverviewComparison.from_dict(d.pop("comparison"))




        criterion_columns = cast(list[str], d.pop("criterion_columns"))


        criterion_series = []
        _criterion_series = d.pop("criterion_series")
        for criterion_series_item_data in (_criterion_series):
            criterion_series_item = ManagedAgentsCriterionSeriesPoint.from_dict(criterion_series_item_data)



            criterion_series.append(criterion_series_item)


        from_ = datetime.datetime.fromisoformat(d.pop("from"))




        prior_from = datetime.datetime.fromisoformat(d.pop("prior_from"))




        prior_to = datetime.datetime.fromisoformat(d.pop("prior_to"))




        tiles = ManagedAgentsEvaluationOverviewTiles.from_dict(d.pop("tiles"))




        to = datetime.datetime.fromisoformat(d.pop("to"))




        _criterion_series_granularity = d.pop("criterion_series_granularity", UNSET)
        criterion_series_granularity: ManagedAgentsEvaluationOverviewResponseCriterionSeriesGranularity | Unset
        if isinstance(_criterion_series_granularity,  Unset):
            criterion_series_granularity = UNSET
        else:
            criterion_series_granularity = ManagedAgentsEvaluationOverviewResponseCriterionSeriesGranularity(_criterion_series_granularity)




        next_page_token = d.pop("next_page_token", UNSET)

        managed_agents_evaluation_overview_response = cls(
            agent_rows=agent_rows,
            as_of=as_of,
            change_markers=change_markers,
            change_markers_status=change_markers_status,
            comparison=comparison,
            criterion_columns=criterion_columns,
            criterion_series=criterion_series,
            from_=from_,
            prior_from=prior_from,
            prior_to=prior_to,
            tiles=tiles,
            to=to,
            criterion_series_granularity=criterion_series_granularity,
            next_page_token=next_page_token,
        )

        return managed_agents_evaluation_overview_response

