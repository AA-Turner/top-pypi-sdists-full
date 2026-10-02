from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_scalar_tiles_data_tiles_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItem





T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesData")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesData:
    """ Scalar-tiles payload: the row of headline tiles.

        Attributes:
            tiles (list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItem]): Ordered
                tiles rendered left to right.
     """

    tiles: list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_scalar_tiles_data_tiles_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItem # noqa: PLC0415
        tiles = []
        for tiles_item_data in self.tiles:
            tiles_item = tiles_item_data.to_dict()
            tiles.append(tiles_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "tiles": tiles,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_scalar_tiles_data_tiles_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItem # noqa: PLC0415
        d = dict(src_dict)
        tiles = []
        _tiles = d.pop("tiles")
        for tiles_item_data in (_tiles):
            tiles_item = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItem.from_dict(tiles_item_data)



            tiles.append(tiles_item)


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_scalar_tiles_data = cls(
            tiles=tiles,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_scalar_tiles_data

