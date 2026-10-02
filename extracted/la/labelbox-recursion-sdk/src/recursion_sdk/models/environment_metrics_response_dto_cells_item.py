from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.environment_metrics_response_dto_cells_item_attempts_item import EnvironmentMetricsResponseDtoCellsItemAttemptsItem





T = TypeVar("T", bound="EnvironmentMetricsResponseDtoCellsItem")



@_attrs_define
class EnvironmentMetricsResponseDtoCellsItem:
    """ Aggregated metrics for one (model, problem-version) pair within an environment.

        Attributes:
            model_id (str): api_model_name value identifying the model that produced these runs.
            problem_version_id (UUID): Problem version these runs target.
            total_cost_usd (float | None): Sum of run costs in USD over the same ≤500 most-recent runs sampled per cell as
                the attempts array, or null when cost data is absent.
            attempts (list[EnvironmentMetricsResponseDtoCellsItemAttemptsItem]): Per-attempt (score, status) data for
                dynamic tau and score-distribution charts, capped at 500 most-recent per cell.
     """

    model_id: str
    problem_version_id: UUID
    total_cost_usd: float | None
    attempts: list[EnvironmentMetricsResponseDtoCellsItemAttemptsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.environment_metrics_response_dto_cells_item_attempts_item import EnvironmentMetricsResponseDtoCellsItemAttemptsItem # noqa: PLC0415
        model_id = self.model_id

        problem_version_id = str(self.problem_version_id)

        total_cost_usd: float | None
        total_cost_usd = self.total_cost_usd

        attempts = []
        for attempts_item_data in self.attempts:
            attempts_item = attempts_item_data.to_dict()
            attempts.append(attempts_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "modelId": model_id,
            "problemVersionId": problem_version_id,
            "totalCostUsd": total_cost_usd,
            "attempts": attempts,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.environment_metrics_response_dto_cells_item_attempts_item import EnvironmentMetricsResponseDtoCellsItemAttemptsItem # noqa: PLC0415
        d = dict(src_dict)
        model_id = d.pop("modelId")

        problem_version_id = UUID(d.pop("problemVersionId"))




        def _parse_total_cost_usd(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        total_cost_usd = _parse_total_cost_usd(d.pop("totalCostUsd"))


        attempts = []
        _attempts = d.pop("attempts")
        for attempts_item_data in (_attempts):
            attempts_item = EnvironmentMetricsResponseDtoCellsItemAttemptsItem.from_dict(attempts_item_data)



            attempts.append(attempts_item)


        environment_metrics_response_dto_cells_item = cls(
            model_id=model_id,
            problem_version_id=problem_version_id,
            total_cost_usd=total_cost_usd,
            attempts=attempts,
        )

        return environment_metrics_response_dto_cells_item

