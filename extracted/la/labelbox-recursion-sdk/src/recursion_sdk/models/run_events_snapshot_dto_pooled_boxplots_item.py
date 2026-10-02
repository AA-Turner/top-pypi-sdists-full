from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_pooled_boxplots_item_summary import RunEventsSnapshotDtoPooledBoxplotsItemSummary





T = TypeVar("T", bound="RunEventsSnapshotDtoPooledBoxplotsItem")



@_attrs_define
class RunEventsSnapshotDtoPooledBoxplotsItem:
    """ Backend-computed pooled five-number summary for one boxplot-block title, recomputed from every fetched step's raw
    group_stds concatenated together.

        Attributes:
            title (str): Boxplot-block title this pooled summary was computed for.
            subtitle (None | str): Boxplot-block subtitle, when the source block carried one.
            summary (RunEventsSnapshotDtoPooledBoxplotsItemSummary): Box-plot five-number summary (min/q1/median/q3/max)
                plus Tukey-fence outliers.
            mean (float | None): Mean of the pooled group_stds, or null when empty.
            n (int): Count of raw group_stds values pooled across all fetched steps.
     """

    title: str
    subtitle: None | str
    summary: RunEventsSnapshotDtoPooledBoxplotsItemSummary
    mean: float | None
    n: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_pooled_boxplots_item_summary import RunEventsSnapshotDtoPooledBoxplotsItemSummary # noqa: PLC0415
        title = self.title

        subtitle: None | str
        subtitle = self.subtitle

        summary = self.summary.to_dict()

        mean: float | None
        mean = self.mean

        n = self.n


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "title": title,
            "subtitle": subtitle,
            "summary": summary,
            "mean": mean,
            "n": n,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_pooled_boxplots_item_summary import RunEventsSnapshotDtoPooledBoxplotsItemSummary # noqa: PLC0415
        d = dict(src_dict)
        title = d.pop("title")

        def _parse_subtitle(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        subtitle = _parse_subtitle(d.pop("subtitle"))


        summary = RunEventsSnapshotDtoPooledBoxplotsItemSummary.from_dict(d.pop("summary"))




        def _parse_mean(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        mean = _parse_mean(d.pop("mean"))


        n = d.pop("n")

        run_events_snapshot_dto_pooled_boxplots_item = cls(
            title=title,
            subtitle=subtitle,
            summary=summary,
            mean=mean,
            n=n,
        )

        return run_events_snapshot_dto_pooled_boxplots_item

