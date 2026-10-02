from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_table_page_type import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_table_page_data import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageData





T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePage")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePage:
    """ Descriptor for a table-page block; the actual rows are paginated lazily elsewhere, never inlined in this document.

        Attributes:
            title (str): Trainer-authored title shown above the rendered block.
            type_ (RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageType): Block-type discriminant.
            data (RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageData): Table-page payload: metadata
                describing where rows are fetched lazily from.
            subtitle (None | str | Unset): Optional trainer-authored subtitle for the block.
     """

    title: str
    type_: RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageType
    data: RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageData
    subtitle: None | str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_table_page_data import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageData # noqa: PLC0415
        title = self.title

        type_ = self.type_.value

        data = self.data.to_dict()

        subtitle: None | str | Unset
        if isinstance(self.subtitle, Unset):
            subtitle = UNSET
        else:
            subtitle = self.subtitle


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "title": title,
            "type": type_,
            "data": data,
        })
        if subtitle is not UNSET:
            field_dict["subtitle"] = subtitle

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_table_page_data import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageData # noqa: PLC0415
        d = dict(src_dict)
        title = d.pop("title")

        type_ = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageType(d.pop("type"))




        data = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageData.from_dict(d.pop("data"))




        def _parse_subtitle(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        subtitle = _parse_subtitle(d.pop("subtitle", UNSET))


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_table_page = cls(
            title=title,
            type_=type_,
            data=data,
            subtitle=subtitle,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_table_page

