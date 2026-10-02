from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataBoxesItem")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataBoxesItem:
    """ One precomputed Tukey box (quartiles + whiskers + outliers) for a boxplot block.

        Attributes:
            label (str): Category label for this box.
            lo (float): Minimum observed value in the box category.
            q1 (float): First quartile (25th percentile).
            median (float): Median (50th percentile).
            q3 (float): Third quartile (75th percentile).
            hi (float): Maximum observed value in the box category.
            whisker_lo (float): Lower Tukey-fence whisker endpoint.
            whisker_hi (float): Upper Tukey-fence whisker endpoint.
            outliers (list[float]): Values beyond the whiskers.
     """

    label: str
    lo: float
    q1: float
    median: float
    q3: float
    hi: float
    whisker_lo: float
    whisker_hi: float
    outliers: list[float]





    def to_dict(self) -> dict[str, Any]:
        label = self.label

        lo = self.lo

        q1 = self.q1

        median = self.median

        q3 = self.q3

        hi = self.hi

        whisker_lo = self.whisker_lo

        whisker_hi = self.whisker_hi

        outliers = self.outliers




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "label": label,
            "lo": lo,
            "q1": q1,
            "median": median,
            "q3": q3,
            "hi": hi,
            "whisker_lo": whisker_lo,
            "whisker_hi": whisker_hi,
            "outliers": outliers,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        lo = d.pop("lo")

        q1 = d.pop("q1")

        median = d.pop("median")

        q3 = d.pop("q3")

        hi = d.pop("hi")

        whisker_lo = d.pop("whisker_lo")

        whisker_hi = d.pop("whisker_hi")

        outliers = cast(list[float], d.pop("outliers"))


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot_data_boxes_item = cls(
            label=label,
            lo=lo,
            q1=q1,
            median=median,
            q3=q3,
            hi=hi,
            whisker_lo=whisker_lo,
            whisker_hi=whisker_hi,
            outliers=outliers,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot_data_boxes_item

