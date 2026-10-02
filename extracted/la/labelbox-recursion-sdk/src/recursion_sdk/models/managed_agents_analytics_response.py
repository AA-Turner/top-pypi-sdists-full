from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_analytics_response_granularity import ManagedAgentsAnalyticsResponseGranularity
from ..models.managed_agents_analytics_response_scope import ManagedAgentsAnalyticsResponseScope
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_analytics_breakdown import ManagedAgentsAnalyticsBreakdown
  from ..models.managed_agents_analytics_series_group import ManagedAgentsAnalyticsSeriesGroup
  from ..models.managed_agents_analytics_series_point import ManagedAgentsAnalyticsSeriesPoint
  from ..models.managed_agents_analytics_totals import ManagedAgentsAnalyticsTotals





T = TypeVar("T", bound="ManagedAgentsAnalyticsResponse")



@_attrs_define
class ManagedAgentsAnalyticsResponse:
    """ Pre-aggregated analytics for one metric family, scope, and time window. Figures are read from a maintained
    projection rather than from session events, so a response is bounded regardless of how much history the organization
    has, and states its own freshness through as_of and lag_seconds.

        Example:
            {'as_of': '2026-02-18T09:30:00Z', 'breakdowns': [{'dimension': 'example', 'rows': [{'cache_read_tokens': 1,
                'cache_write_tokens': 1, 'criterion_count': 1, 'criterion_fail_count': 1, 'criterion_not_applicable_count': 1,
                'criterion_pass_count': 1, 'criterion_pass_rate': 1.5, 'duration_samples': 1, 'environment_failed': 1,
                'environment_ready': 1, 'environment_starts': 1, 'environment_startup_ms': 1, 'evaluation_count': 1,
                'evaluation_fail_count': 1, 'evaluation_not_applicable_count': 1, 'evaluation_pass_count': 1,
                'evaluation_pass_rate': 1.5, 'event_count': 1, 'input_tokens': 1, 'label': 'example', 'model_calls': 1,
                'model_cost_micros': 1, 'output_tokens': 1, 'p50_ms': 1.5, 'p90_ms': 1.5, 'p95_ms': 1.5,
                'session_completion_ms': 1, 'sessions': 1, 'tool_calls': 1, 'tool_completed': 1, 'tool_cost_micros': 1,
                'tool_duration_ms': 1, 'tool_failed': 1, 'tool_in_flight': 1, 'total_cost_micros': 1, 'turns': 1, 'value':
                'example'}]}], 'family': 'example', 'family_version': 1, 'from': '2026-02-18T09:30:00Z', 'granularity': 'hour',
                'lag_seconds': 1, 'scope': 'workspace', 'series': [{'bucket_start': '2026-02-18T09:30:00Z', 'cache_read_tokens':
                1, 'cache_write_tokens': 1, 'criterion_count': 1, 'criterion_fail_count': 1, 'criterion_not_applicable_count':
                1, 'criterion_pass_count': 1, 'criterion_pass_rate': 1.5, 'duration_samples': 1, 'environment_failed': 1,
                'environment_ready': 1, 'environment_starts': 1, 'environment_startup_ms': 1, 'evaluation_count': 1,
                'evaluation_fail_count': 1, 'evaluation_not_applicable_count': 1, 'evaluation_pass_count': 1,
                'evaluation_pass_rate': 1.5, 'event_count': 1, 'input_tokens': 1, 'model_calls': 1, 'model_cost_micros': 1,
                'output_tokens': 1, 'p50_ms': 1.5, 'p90_ms': 1.5, 'p95_ms': 1.5, 'session_completion_ms': 1, 'sessions': 1,
                'tool_calls': 1, 'tool_completed': 1, 'tool_cost_micros': 1, 'tool_duration_ms': 1, 'tool_failed': 1,
                'tool_in_flight': 1, 'total_cost_micros': 1, 'turns': 1}], 'series_group_by': 'example', 'series_groups':
                [{'label': 'example', 'points': [{'bucket_start': '2026-02-18T09:30:00Z', 'cache_read_tokens': 1,
                'cache_write_tokens': 1, 'criterion_count': 1, 'criterion_fail_count': 1, 'criterion_not_applicable_count': 1,
                'criterion_pass_count': 1, 'criterion_pass_rate': 1.5, 'duration_samples': 1, 'environment_failed': 1,
                'environment_ready': 1, 'environment_starts': 1, 'environment_startup_ms': 1, 'evaluation_count': 1,
                'evaluation_fail_count': 1, 'evaluation_not_applicable_count': 1, 'evaluation_pass_count': 1,
                'evaluation_pass_rate': 1.5, 'event_count': 1, 'input_tokens': 1, 'model_calls': 1, 'model_cost_micros': 1,
                'output_tokens': 1, 'p50_ms': 1.5, 'p90_ms': 1.5, 'p95_ms': 1.5, 'session_completion_ms': 1, 'sessions': 1,
                'tool_calls': 1, 'tool_completed': 1, 'tool_cost_micros': 1, 'tool_duration_ms': 1, 'tool_failed': 1,
                'tool_in_flight': 1, 'total_cost_micros': 1, 'turns': 1}], 'value': 'example'}], 'to': '2026-02-18T09:30:00Z',
                'totals': {'cache_read_tokens': 1, 'cache_write_tokens': 1, 'criterion_count': 1, 'criterion_fail_count': 1,
                'criterion_not_applicable_count': 1, 'criterion_pass_count': 1, 'criterion_pass_rate': 1.5, 'duration_samples':
                1, 'environment_failed': 1, 'environment_ready': 1, 'environment_starts': 1, 'environment_startup_ms': 1,
                'evaluation_count': 1, 'evaluation_fail_count': 1, 'evaluation_not_applicable_count': 1,
                'evaluation_pass_count': 1, 'evaluation_pass_rate': 1.5, 'event_count': 1, 'input_tokens': 1, 'model_calls': 1,
                'model_cost_micros': 1, 'output_tokens': 1, 'p50_ms': 1.5, 'p90_ms': 1.5, 'p95_ms': 1.5,
                'session_completion_ms': 1, 'sessions': 1, 'tool_calls': 1, 'tool_completed': 1, 'tool_cost_micros': 1,
                'tool_duration_ms': 1, 'tool_failed': 1, 'tool_in_flight': 1, 'total_cost_micros': 1, 'turns': 1}}

        Attributes:
            as_of (datetime.datetime): How current these figures are: the projector's durable watermark. Work committed
                after this instant is not included yet.
            breakdowns (list[ManagedAgentsAnalyticsBreakdown] | None): The family's default groupings, each capped by limit.
            family (str): Metric family these figures come from.
            family_version (int): Active version of the family's projection. A change here means the underlying derivation
                changed.
            from_ (datetime.datetime): Inclusive start actually aggregated, widened outward to a bucket boundary.
            granularity (ManagedAgentsAnalyticsResponseGranularity): Width of each series bucket. Chosen from the window:
                hourly up to two days, daily beyond that.
            lag_seconds (int): Seconds between as_of and now. A steady value under a minute is normal; a growing one means
                the projector is behind.
            scope (ManagedAgentsAnalyticsResponseScope): Read locality the figures were aggregated at, after authorization.
                This may be narrower than the scope requested.
            series (list[ManagedAgentsAnalyticsSeriesPoint] | None): One point per time bucket, ascending. Buckets with no
                activity are omitted rather than zero-filled.
            to (datetime.datetime): Exclusive end actually aggregated, widened outward to a bucket boundary.
            totals (ManagedAgentsAnalyticsTotals): Aggregated analytics measures for one window, group, or time bucket.
                Counters and sums are exact; p50_ms, p90_ms and p95_ms are approximate, derived from a fixed-bin histogram so
                they can be merged across shards, buckets, and scopes. Example: {'cache_read_tokens': 1, 'cache_write_tokens':
                1, 'criterion_count': 1, 'criterion_fail_count': 1, 'criterion_not_applicable_count': 1, 'criterion_pass_count':
                1, 'criterion_pass_rate': 1.5, 'duration_samples': 1, 'environment_failed': 1, 'environment_ready': 1,
                'environment_starts': 1, 'environment_startup_ms': 1, 'evaluation_count': 1, 'evaluation_fail_count': 1,
                'evaluation_not_applicable_count': 1, 'evaluation_pass_count': 1, 'evaluation_pass_rate': 1.5, 'event_count': 1,
                'input_tokens': 1, 'model_calls': 1, 'model_cost_micros': 1, 'output_tokens': 1, 'p50_ms': 1.5, 'p90_ms': 1.5,
                'p95_ms': 1.5, 'session_completion_ms': 1, 'sessions': 1, 'tool_calls': 1, 'tool_completed': 1,
                'tool_cost_micros': 1, 'tool_duration_ms': 1, 'tool_failed': 1, 'tool_in_flight': 1, 'total_cost_micros': 1,
                'turns': 1}.
            series_group_by (str | Unset): Dimension series_groups is split by, echoing the request. Absent when no stacked
                series was asked for.
            series_groups (list[ManagedAgentsAnalyticsSeriesGroup] | Unset): One band per dimension value, for a stacked
                chart. Present only when series_group_by was requested.
     """

    as_of: datetime.datetime
    breakdowns: list[ManagedAgentsAnalyticsBreakdown] | None
    family: str
    family_version: int
    from_: datetime.datetime
    granularity: ManagedAgentsAnalyticsResponseGranularity
    lag_seconds: int
    scope: ManagedAgentsAnalyticsResponseScope
    series: list[ManagedAgentsAnalyticsSeriesPoint] | None
    to: datetime.datetime
    totals: ManagedAgentsAnalyticsTotals
    series_group_by: str | Unset = UNSET
    series_groups: list[ManagedAgentsAnalyticsSeriesGroup] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_analytics_breakdown import ManagedAgentsAnalyticsBreakdown # noqa: PLC0415
        from ..models.managed_agents_analytics_series_group import ManagedAgentsAnalyticsSeriesGroup # noqa: PLC0415
        from ..models.managed_agents_analytics_series_point import ManagedAgentsAnalyticsSeriesPoint # noqa: PLC0415
        from ..models.managed_agents_analytics_totals import ManagedAgentsAnalyticsTotals # noqa: PLC0415
        as_of = self.as_of.isoformat()

        breakdowns: list[dict[str, Any]] | None
        if isinstance(self.breakdowns, list):
            breakdowns = []
            for breakdowns_type_0_item_data in self.breakdowns:
                breakdowns_type_0_item = breakdowns_type_0_item_data.to_dict()
                breakdowns.append(breakdowns_type_0_item)


        else:
            breakdowns = self.breakdowns

        family = self.family

        family_version = self.family_version

        from_ = self.from_.isoformat()

        granularity = self.granularity.value

        lag_seconds = self.lag_seconds

        scope = self.scope.value

        series: list[dict[str, Any]] | None
        if isinstance(self.series, list):
            series = []
            for series_type_0_item_data in self.series:
                series_type_0_item = series_type_0_item_data.to_dict()
                series.append(series_type_0_item)


        else:
            series = self.series

        to = self.to.isoformat()

        totals = self.totals.to_dict()

        series_group_by = self.series_group_by

        series_groups: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.series_groups, Unset):
            series_groups = []
            for series_groups_item_data in self.series_groups:
                series_groups_item = series_groups_item_data.to_dict()
                series_groups.append(series_groups_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "as_of": as_of,
            "breakdowns": breakdowns,
            "family": family,
            "family_version": family_version,
            "from": from_,
            "granularity": granularity,
            "lag_seconds": lag_seconds,
            "scope": scope,
            "series": series,
            "to": to,
            "totals": totals,
        })
        if series_group_by is not UNSET:
            field_dict["series_group_by"] = series_group_by
        if series_groups is not UNSET:
            field_dict["series_groups"] = series_groups

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_analytics_breakdown import ManagedAgentsAnalyticsBreakdown # noqa: PLC0415
        from ..models.managed_agents_analytics_series_group import ManagedAgentsAnalyticsSeriesGroup # noqa: PLC0415
        from ..models.managed_agents_analytics_series_point import ManagedAgentsAnalyticsSeriesPoint # noqa: PLC0415
        from ..models.managed_agents_analytics_totals import ManagedAgentsAnalyticsTotals # noqa: PLC0415
        d = dict(src_dict)
        as_of = datetime.datetime.fromisoformat(d.pop("as_of"))




        def _parse_breakdowns(data: object) -> list[ManagedAgentsAnalyticsBreakdown] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                breakdowns_type_0 = []
                _breakdowns_type_0 = data
                for breakdowns_type_0_item_data in (_breakdowns_type_0):
                    breakdowns_type_0_item = ManagedAgentsAnalyticsBreakdown.from_dict(breakdowns_type_0_item_data)



                    breakdowns_type_0.append(breakdowns_type_0_item)

                return breakdowns_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAnalyticsBreakdown] | None, data)

        breakdowns = _parse_breakdowns(d.pop("breakdowns"))


        family = d.pop("family")

        family_version = d.pop("family_version")

        from_ = datetime.datetime.fromisoformat(d.pop("from"))




        granularity = ManagedAgentsAnalyticsResponseGranularity(d.pop("granularity"))




        lag_seconds = d.pop("lag_seconds")

        scope = ManagedAgentsAnalyticsResponseScope(d.pop("scope"))




        def _parse_series(data: object) -> list[ManagedAgentsAnalyticsSeriesPoint] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                series_type_0 = []
                _series_type_0 = data
                for series_type_0_item_data in (_series_type_0):
                    series_type_0_item = ManagedAgentsAnalyticsSeriesPoint.from_dict(series_type_0_item_data)



                    series_type_0.append(series_type_0_item)

                return series_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAnalyticsSeriesPoint] | None, data)

        series = _parse_series(d.pop("series"))


        to = datetime.datetime.fromisoformat(d.pop("to"))




        totals = ManagedAgentsAnalyticsTotals.from_dict(d.pop("totals"))




        series_group_by = d.pop("series_group_by", UNSET)

        _series_groups = d.pop("series_groups", UNSET)
        series_groups: list[ManagedAgentsAnalyticsSeriesGroup] | Unset = UNSET
        if _series_groups is not UNSET:
            series_groups = []
            for series_groups_item_data in _series_groups:
                series_groups_item = ManagedAgentsAnalyticsSeriesGroup.from_dict(series_groups_item_data)



                series_groups.append(series_groups_item)


        managed_agents_analytics_response = cls(
            as_of=as_of,
            breakdowns=breakdowns,
            family=family,
            family_version=family_version,
            from_=from_,
            granularity=granularity,
            lag_seconds=lag_seconds,
            scope=scope,
            series=series,
            to=to,
            totals=totals,
            series_group_by=series_group_by,
            series_groups=series_groups,
        )


        managed_agents_analytics_response.additional_properties = d
        return managed_agents_analytics_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
