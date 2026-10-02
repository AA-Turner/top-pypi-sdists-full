from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.rollout_batch_results_response_dto_output_type_0_verdict import RolloutBatchResultsResponseDtoOutputType0Verdict
from typing import cast






T = TypeVar("T", bound="RolloutBatchResultsResponseDtoOutputType0")



@_attrs_define
class RolloutBatchResultsResponseDtoOutputType0:
    """ Aggregate result of a completed rollout_batch: rollout tallies, verdict, total cost.

        Attributes:
            total_rollouts (int): Total M x N rollouts in the batch.
            completed_rollouts (int): Rollouts that completed successfully.
            failed_rollouts (int): Rollouts that did not complete successfully.
            verdict (RolloutBatchResultsResponseDtoOutputType0Verdict): completed: every rollout succeeded. partial: some
                succeeded. failed: none succeeded.
            total_cost (float | None): Sum of every rollout that reported a cost; null if none did.
     """

    total_rollouts: int
    completed_rollouts: int
    failed_rollouts: int
    verdict: RolloutBatchResultsResponseDtoOutputType0Verdict
    total_cost: float | None





    def to_dict(self) -> dict[str, Any]:
        total_rollouts = self.total_rollouts

        completed_rollouts = self.completed_rollouts

        failed_rollouts = self.failed_rollouts

        verdict = self.verdict.value

        total_cost: float | None
        total_cost = self.total_cost


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "totalRollouts": total_rollouts,
            "completedRollouts": completed_rollouts,
            "failedRollouts": failed_rollouts,
            "verdict": verdict,
            "totalCost": total_cost,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_rollouts = d.pop("totalRollouts")

        completed_rollouts = d.pop("completedRollouts")

        failed_rollouts = d.pop("failedRollouts")

        verdict = RolloutBatchResultsResponseDtoOutputType0Verdict(d.pop("verdict"))




        def _parse_total_cost(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        total_cost = _parse_total_cost(d.pop("totalCost"))


        rollout_batch_results_response_dto_output_type_0 = cls(
            total_rollouts=total_rollouts,
            completed_rollouts=completed_rollouts,
            failed_rollouts=failed_rollouts,
            verdict=verdict,
            total_cost=total_cost,
        )

        return rollout_batch_results_response_dto_output_type_0

