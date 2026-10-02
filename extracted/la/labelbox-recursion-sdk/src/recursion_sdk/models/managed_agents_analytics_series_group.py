from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_analytics_series_point import ManagedAgentsAnalyticsSeriesPoint





T = TypeVar("T", bound="ManagedAgentsAnalyticsSeriesGroup")



@_attrs_define
class ManagedAgentsAnalyticsSeriesGroup:
    """ One band of a stacked series. Percentiles are omitted on these points: a stacked chart plots additive counts, and
    merging one histogram per group per bucket would cost far more than the picture is worth.

        Example:
            {'label': 'example', 'points': [{'bucket_start': '2026-02-18T09:30:00Z', 'cache_read_tokens': 1,
                'cache_write_tokens': 1, 'criterion_count': 1, 'criterion_fail_count': 1, 'criterion_not_applicable_count': 1,
                'criterion_pass_count': 1, 'criterion_pass_rate': 1.5, 'duration_samples': 1, 'environment_failed': 1,
                'environment_ready': 1, 'environment_starts': 1, 'environment_startup_ms': 1, 'evaluation_count': 1,
                'evaluation_fail_count': 1, 'evaluation_not_applicable_count': 1, 'evaluation_pass_count': 1,
                'evaluation_pass_rate': 1.5, 'event_count': 1, 'input_tokens': 1, 'model_calls': 1, 'model_cost_micros': 1,
                'output_tokens': 1, 'p50_ms': 1.5, 'p90_ms': 1.5, 'p95_ms': 1.5, 'session_completion_ms': 1, 'sessions': 1,
                'tool_calls': 1, 'tool_completed': 1, 'tool_cost_micros': 1, 'tool_duration_ms': 1, 'tool_failed': 1,
                'tool_in_flight': 1, 'total_cost_micros': 1, 'turns': 1}], 'value': 'example'}

        Attributes:
            points (list[ManagedAgentsAnalyticsSeriesPoint] | None): This line's buckets, ascending. Buckets where this
                group recorded nothing are omitted, so a stacked chart must zero-fill them.
            value (str): The dimension's value for this line, and the value to pass back as a filter. Empty means the
                dimension was not recorded on the underlying work.
            label (str | Unset): Human-readable name for value, resolved when the request is served, on the same terms as a
                breakdown row's label.
     """

    points: list[ManagedAgentsAnalyticsSeriesPoint] | None
    value: str
    label: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_analytics_series_point import ManagedAgentsAnalyticsSeriesPoint # noqa: PLC0415
        points: list[dict[str, Any]] | None
        if isinstance(self.points, list):
            points = []
            for points_type_0_item_data in self.points:
                points_type_0_item = points_type_0_item_data.to_dict()
                points.append(points_type_0_item)


        else:
            points = self.points

        value = self.value

        label = self.label


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "points": points,
            "value": value,
        })
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_analytics_series_point import ManagedAgentsAnalyticsSeriesPoint # noqa: PLC0415
        d = dict(src_dict)
        def _parse_points(data: object) -> list[ManagedAgentsAnalyticsSeriesPoint] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                points_type_0 = []
                _points_type_0 = data
                for points_type_0_item_data in (_points_type_0):
                    points_type_0_item = ManagedAgentsAnalyticsSeriesPoint.from_dict(points_type_0_item_data)



                    points_type_0.append(points_type_0_item)

                return points_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAnalyticsSeriesPoint] | None, data)

        points = _parse_points(d.pop("points"))


        value = d.pop("value")

        label = d.pop("label", UNSET)

        managed_agents_analytics_series_group = cls(
            points=points,
            value=value,
            label=label,
        )


        managed_agents_analytics_series_group.additional_properties = d
        return managed_agents_analytics_series_group

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
