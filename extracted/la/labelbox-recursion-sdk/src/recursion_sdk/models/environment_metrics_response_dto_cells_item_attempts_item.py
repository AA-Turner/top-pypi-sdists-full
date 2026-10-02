from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.environment_metrics_response_dto_cells_item_attempts_item_status import EnvironmentMetricsResponseDtoCellsItemAttemptsItemStatus
from typing import cast






T = TypeVar("T", bound="EnvironmentMetricsResponseDtoCellsItemAttemptsItem")



@_attrs_define
class EnvironmentMetricsResponseDtoCellsItemAttemptsItem:
    """ Minimal per-attempt data used by the frontend to compute dynamic tau sweeps.

        Attributes:
            score (float | None): Graded score for this attempt, or null if unscored.
            status (EnvironmentMetricsResponseDtoCellsItemAttemptsItemStatus): Terminal or in-flight status of this problem
                run.
     """

    score: float | None
    status: EnvironmentMetricsResponseDtoCellsItemAttemptsItemStatus





    def to_dict(self) -> dict[str, Any]:
        score: float | None
        score = self.score

        status = self.status.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "score": score,
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        score = _parse_score(d.pop("score"))


        status = EnvironmentMetricsResponseDtoCellsItemAttemptsItemStatus(d.pop("status"))




        environment_metrics_response_dto_cells_item_attempts_item = cls(
            score=score,
            status=status,
        )

        return environment_metrics_response_dto_cells_item_attempts_item

