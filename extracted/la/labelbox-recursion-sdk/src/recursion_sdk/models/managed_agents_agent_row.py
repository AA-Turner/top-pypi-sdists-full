from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.managed_agents_newest_failure import ManagedAgentsNewestFailure
  from ..models.managed_agents_verdict_metric import ManagedAgentsVerdictMetric





T = TypeVar("T", bound="ManagedAgentsAgentRow")



@_attrs_define
class ManagedAgentsAgentRow:
    """ One target-agent row with overall and aligned criterion metrics plus newest failures.

        Example:
            {'criterion_metrics': [None], 'evaluation_count': 1, 'newest_failures': [{'created_at': '2026-02-18T09:30:00Z',
                'evaluation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'failed_criterion_keys': ['example'],
                'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_available': True,
                'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'overall_pass': {'delta_pp': 1.5, 'fail_count':
                1, 'not_applicable_count': 1, 'pass_count': 1, 'prior_rate': 1, 'rate': 1}, 'target_agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            criterion_metrics (list[ManagedAgentsVerdictMetric | None]): Metrics aligned positionally with
                criterion_columns; null marks no observations for that key.
            evaluation_count (int): Immutable evaluation snapshots for this target agent in the current window.
            newest_failures (list[ManagedAgentsNewestFailure]): Up to three newest failing evaluations for this target
                agent.
            overall_pass (ManagedAgentsVerdictMetric): Pass, fail, not-applicable, rate, and adjacent-window comparison for
                one verdict population. Example: {'delta_pp': 1.5, 'fail_count': 1, 'not_applicable_count': 1, 'pass_count': 1,
                'prior_rate': 1, 'rate': 1}.
            target_agent_id (UUID): Target agent represented by this Overview table row.
     """

    criterion_metrics: list[ManagedAgentsVerdictMetric | None]
    evaluation_count: int
    newest_failures: list[ManagedAgentsNewestFailure]
    overall_pass: ManagedAgentsVerdictMetric
    target_agent_id: UUID





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_newest_failure import ManagedAgentsNewestFailure # noqa: PLC0415
        from ..models.managed_agents_verdict_metric import ManagedAgentsVerdictMetric # noqa: PLC0415
        criterion_metrics = []
        for criterion_metrics_item_data in self.criterion_metrics:
            criterion_metrics_item: dict[str, Any] | None
            if isinstance(criterion_metrics_item_data, ManagedAgentsVerdictMetric):
                criterion_metrics_item = criterion_metrics_item_data.to_dict()
            else:
                criterion_metrics_item = criterion_metrics_item_data
            criterion_metrics.append(criterion_metrics_item)



        evaluation_count = self.evaluation_count

        newest_failures = []
        for newest_failures_item_data in self.newest_failures:
            newest_failures_item = newest_failures_item_data.to_dict()
            newest_failures.append(newest_failures_item)



        overall_pass = self.overall_pass.to_dict()

        target_agent_id = str(self.target_agent_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "criterion_metrics": criterion_metrics,
            "evaluation_count": evaluation_count,
            "newest_failures": newest_failures,
            "overall_pass": overall_pass,
            "target_agent_id": target_agent_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_newest_failure import ManagedAgentsNewestFailure # noqa: PLC0415
        from ..models.managed_agents_verdict_metric import ManagedAgentsVerdictMetric # noqa: PLC0415
        d = dict(src_dict)
        criterion_metrics = []
        _criterion_metrics = d.pop("criterion_metrics")
        for criterion_metrics_item_data in (_criterion_metrics):
            def _parse_criterion_metrics_item(data: object) -> ManagedAgentsVerdictMetric | None:
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    criterion_metrics_item_type_1 = ManagedAgentsVerdictMetric.from_dict(data)



                    return criterion_metrics_item_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                return cast(ManagedAgentsVerdictMetric | None, data)

            criterion_metrics_item = _parse_criterion_metrics_item(criterion_metrics_item_data)

            criterion_metrics.append(criterion_metrics_item)


        evaluation_count = d.pop("evaluation_count")

        newest_failures = []
        _newest_failures = d.pop("newest_failures")
        for newest_failures_item_data in (_newest_failures):
            newest_failures_item = ManagedAgentsNewestFailure.from_dict(newest_failures_item_data)



            newest_failures.append(newest_failures_item)


        overall_pass = ManagedAgentsVerdictMetric.from_dict(d.pop("overall_pass"))




        target_agent_id = UUID(d.pop("target_agent_id"))




        managed_agents_agent_row = cls(
            criterion_metrics=criterion_metrics,
            evaluation_count=evaluation_count,
            newest_failures=newest_failures,
            overall_pass=overall_pass,
            target_agent_id=target_agent_id,
        )

        return managed_agents_agent_row

