from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_analytics_breakdown_row import ManagedAgentsAnalyticsBreakdownRow





T = TypeVar("T", bound="ManagedAgentsAnalyticsBreakdown")



@_attrs_define
class ManagedAgentsAnalyticsBreakdown:
    """ One dimension's groups for the requested window. Which dimensions appear is chosen by the family and the scope: a
    tenant or global read leads with workspace, since that is the question the narrower groupings cannot answer.

        Example:
            {'dimension': 'example', 'rows': [{'cache_read_tokens': 1, 'cache_write_tokens': 1, 'criterion_count': 1,
                'criterion_fail_count': 1, 'criterion_not_applicable_count': 1, 'criterion_pass_count': 1,
                'criterion_pass_rate': 1.5, 'duration_samples': 1, 'environment_failed': 1, 'environment_ready': 1,
                'environment_starts': 1, 'environment_startup_ms': 1, 'evaluation_count': 1, 'evaluation_fail_count': 1,
                'evaluation_not_applicable_count': 1, 'evaluation_pass_count': 1, 'evaluation_pass_rate': 1.5, 'event_count': 1,
                'input_tokens': 1, 'label': 'example', 'model_calls': 1, 'model_cost_micros': 1, 'output_tokens': 1, 'p50_ms':
                1.5, 'p90_ms': 1.5, 'p95_ms': 1.5, 'session_completion_ms': 1, 'sessions': 1, 'tool_calls': 1, 'tool_completed':
                1, 'tool_cost_micros': 1, 'tool_duration_ms': 1, 'tool_failed': 1, 'tool_in_flight': 1, 'total_cost_micros': 1,
                'turns': 1, 'value': 'example'}]}

        Attributes:
            dimension (str): Dimension these rows are grouped by, e.g. tool_name, executing_agent_id, model,
                sandbox_provider, or compute_class.
            rows (list[ManagedAgentsAnalyticsBreakdownRow] | None): Groups ordered by the family's ranking measure,
                descending, capped by limit.
     """

    dimension: str
    rows: list[ManagedAgentsAnalyticsBreakdownRow] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_analytics_breakdown_row import ManagedAgentsAnalyticsBreakdownRow # noqa: PLC0415
        dimension = self.dimension

        rows: list[dict[str, Any]] | None
        if isinstance(self.rows, list):
            rows = []
            for rows_type_0_item_data in self.rows:
                rows_type_0_item = rows_type_0_item_data.to_dict()
                rows.append(rows_type_0_item)


        else:
            rows = self.rows


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "dimension": dimension,
            "rows": rows,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_analytics_breakdown_row import ManagedAgentsAnalyticsBreakdownRow # noqa: PLC0415
        d = dict(src_dict)
        dimension = d.pop("dimension")

        def _parse_rows(data: object) -> list[ManagedAgentsAnalyticsBreakdownRow] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                rows_type_0 = []
                _rows_type_0 = data
                for rows_type_0_item_data in (_rows_type_0):
                    rows_type_0_item = ManagedAgentsAnalyticsBreakdownRow.from_dict(rows_type_0_item_data)



                    rows_type_0.append(rows_type_0_item)

                return rows_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAnalyticsBreakdownRow] | None, data)

        rows = _parse_rows(d.pop("rows"))


        managed_agents_analytics_breakdown = cls(
            dimension=dimension,
            rows=rows,
        )


        managed_agents_analytics_breakdown.additional_properties = d
        return managed_agents_analytics_breakdown

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
