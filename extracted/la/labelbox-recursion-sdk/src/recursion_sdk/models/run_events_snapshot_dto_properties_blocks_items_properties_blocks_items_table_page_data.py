from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_table_page_data_kind import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageDataKind
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageData")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageData:
    """ Table-page payload: metadata describing where rows are fetched lazily from.

        Attributes:
            kind (RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageDataKind): Whether the table holds
                train or eval rows.
            total (int): Total row count available across all pages.
            mean_reward (float | None): Mean reward across the rows, when computable.
            page_size (int): Rows per page used by the lazy row fetch.
            source (str): Opaque identifier of the row source to paginate against.
            columns (list[str] | Unset): Ordered column keys for the paginated rows.
     """

    kind: RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageDataKind
    total: int
    mean_reward: float | None
    page_size: int
    source: str
    columns: list[str] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        total = self.total

        mean_reward: float | None
        mean_reward = self.mean_reward

        page_size = self.page_size

        source = self.source

        columns: list[str] | Unset = UNSET
        if not isinstance(self.columns, Unset):
            columns = self.columns




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "total": total,
            "mean_reward": mean_reward,
            "page_size": page_size,
            "source": source,
        })
        if columns is not UNSET:
            field_dict["columns"] = columns

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageDataKind(d.pop("kind"))




        total = d.pop("total")

        def _parse_mean_reward(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        mean_reward = _parse_mean_reward(d.pop("mean_reward"))


        page_size = d.pop("page_size")

        source = d.pop("source")

        columns = cast(list[str], d.pop("columns", UNSET))


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_table_page_data = cls(
            kind=kind,
            total=total,
            mean_reward=mean_reward,
            page_size=page_size,
            source=source,
            columns=columns,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_table_page_data

