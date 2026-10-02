from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.rollout_batch_results_response_dto_status import RolloutBatchResultsResponseDtoStatus
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.rollout_batch_results_response_dto_output_type_0 import RolloutBatchResultsResponseDtoOutputType0
  from ..models.rollout_batch_results_response_dto_rollouts_item import RolloutBatchResultsResponseDtoRolloutsItem





T = TypeVar("T", bound="RolloutBatchResultsResponseDto")



@_attrs_define
class RolloutBatchResultsResponseDto:
    """ Raw per-rollout results for a rollout_batch: tallies plus one page of child jobs, unshaped.

        Example:
            {'batchId': '11111111-1111-4111-8111-111111111111', 'status': 'completed', 'output': {'totalRollouts': 1,
                'completedRollouts': 1, 'failedRollouts': 0, 'verdict': 'completed', 'totalCost': 0.05}, 'rollouts': [{'id':
                '11111111-1111-4111-8111-111111111111', 'parentJobId': None, 'userId': '11111111-1111-4111-8111-111111111111',
                'type': 'run_config_run', 'name': 'grpo-trainer-run', 'status': 'executing', 'payload': {}, 'externalState':
                None, 'output': None, 'errorMessage': None, 'attempts': 1, 'maxAttempts': 1, 'scheduledAt':
                '2026-01-01T00:00:00.000Z', 'pollAfter': None, 'startedAt': '2026-01-01T00:00:01.000Z', 'completedAt': None,
                'createdAt': '2026-01-01T00:00:00.000Z', 'updatedAt': '2026-01-01T00:00:01.000Z'}], 'nextCursor': None}

        Attributes:
            batch_id (UUID): Stable jobs_v2 identifier (UUID). One row per background-work unit in the generic, strategy-
                driven job framework.
            status (RolloutBatchResultsResponseDtoStatus): Lifecycle state of a jobs_v2 row. Claimable: pending,
                waiting_external (gated by poll_after), aggregating. Parked: executing, waiting_children, cancelling. Terminal:
                completed, failed, cancelled.
            output (None | RolloutBatchResultsResponseDtoOutputType0): Present once the batch itself is terminal-completed;
                null otherwise.
            rollouts (list[RolloutBatchResultsResponseDtoRolloutsItem]): The current page of run_config_run children spawned
                so far, raw and unshaped.
            next_cursor (None | str): Opaque cursor for fetching the next page of rollouts. Null on the last page.
     """

    batch_id: UUID
    status: RolloutBatchResultsResponseDtoStatus
    output: None | RolloutBatchResultsResponseDtoOutputType0
    rollouts: list[RolloutBatchResultsResponseDtoRolloutsItem]
    next_cursor: None | str





    def to_dict(self) -> dict[str, Any]:
        from ..models.rollout_batch_results_response_dto_output_type_0 import RolloutBatchResultsResponseDtoOutputType0 # noqa: PLC0415
        from ..models.rollout_batch_results_response_dto_rollouts_item import RolloutBatchResultsResponseDtoRolloutsItem # noqa: PLC0415
        batch_id = str(self.batch_id)

        status = self.status.value

        output: dict[str, Any] | None
        if isinstance(self.output, RolloutBatchResultsResponseDtoOutputType0):
            output = self.output.to_dict()
        else:
            output = self.output

        rollouts = []
        for rollouts_item_data in self.rollouts:
            rollouts_item = rollouts_item_data.to_dict()
            rollouts.append(rollouts_item)



        next_cursor: None | str
        next_cursor = self.next_cursor


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "batchId": batch_id,
            "status": status,
            "output": output,
            "rollouts": rollouts,
            "nextCursor": next_cursor,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rollout_batch_results_response_dto_output_type_0 import RolloutBatchResultsResponseDtoOutputType0 # noqa: PLC0415
        from ..models.rollout_batch_results_response_dto_rollouts_item import RolloutBatchResultsResponseDtoRolloutsItem # noqa: PLC0415
        d = dict(src_dict)
        batch_id = UUID(d.pop("batchId"))




        status = RolloutBatchResultsResponseDtoStatus(d.pop("status"))




        def _parse_output(data: object) -> None | RolloutBatchResultsResponseDtoOutputType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_0 = RolloutBatchResultsResponseDtoOutputType0.from_dict(data)



                return output_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RolloutBatchResultsResponseDtoOutputType0, data)

        output = _parse_output(d.pop("output"))


        rollouts = []
        _rollouts = d.pop("rollouts")
        for rollouts_item_data in (_rollouts):
            rollouts_item = RolloutBatchResultsResponseDtoRolloutsItem.from_dict(rollouts_item_data)



            rollouts.append(rollouts_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        rollout_batch_results_response_dto = cls(
            batch_id=batch_id,
            status=status,
            output=output,
            rollouts=rollouts,
            next_cursor=next_cursor,
        )

        return rollout_batch_results_response_dto

