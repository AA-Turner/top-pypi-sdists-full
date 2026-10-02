from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.environment_metrics_response_dto_cells_item import EnvironmentMetricsResponseDtoCellsItem





T = TypeVar("T", bound="EnvironmentMetricsResponseDto")



@_attrs_define
class EnvironmentMetricsResponseDto:
    """ Per-model, per-problem-version metric rollup for all problems in an environment.

        Attributes:
            environment_id (UUID): Stable environment identifier (UUID).
            cells (list[EnvironmentMetricsResponseDtoCellsItem]): One entry per (model, problem-version) pair that has at
                least one authoring run.
     """

    environment_id: UUID
    cells: list[EnvironmentMetricsResponseDtoCellsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.environment_metrics_response_dto_cells_item import EnvironmentMetricsResponseDtoCellsItem # noqa: PLC0415
        environment_id = str(self.environment_id)

        cells = []
        for cells_item_data in self.cells:
            cells_item = cells_item_data.to_dict()
            cells.append(cells_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "environmentId": environment_id,
            "cells": cells,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.environment_metrics_response_dto_cells_item import EnvironmentMetricsResponseDtoCellsItem # noqa: PLC0415
        d = dict(src_dict)
        environment_id = UUID(d.pop("environmentId"))




        cells = []
        _cells = d.pop("cells")
        for cells_item_data in (_cells):
            cells_item = EnvironmentMetricsResponseDtoCellsItem.from_dict(cells_item_data)



            cells.append(cells_item)


        environment_metrics_response_dto = cls(
            environment_id=environment_id,
            cells=cells,
        )

        return environment_metrics_response_dto

