from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_scalar_tiles_data_tiles_item_tone_type_0 import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItemToneType0
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItem")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItem:
    """ One tile in a scalar-tiles block: a trainer-authored label + opaque value.

        Attributes:
            label (str): Tile caption shown beside the value.
            value (float | str): Opaque tile value (numeric or preformatted string).
            unit (None | str | Unset): Optional unit suffix rendered after the value.
            delta (float | None | Unset): Optional change-from-previous value for the tile.
            tone (None | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItemToneType0 |
                Unset): Optional color-tone hint for the delta (positive/negative/neutral).
     """

    label: str
    value: float | str
    unit: None | str | Unset = UNSET
    delta: float | None | Unset = UNSET
    tone: None | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItemToneType0 | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        label = self.label

        value: float | str
        value = self.value

        unit: None | str | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        delta: float | None | Unset
        if isinstance(self.delta, Unset):
            delta = UNSET
        else:
            delta = self.delta

        tone: None | str | Unset
        if isinstance(self.tone, Unset):
            tone = UNSET
        elif isinstance(self.tone, RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItemToneType0):
            tone = self.tone.value
        else:
            tone = self.tone


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "label": label,
            "value": value,
        })
        if unit is not UNSET:
            field_dict["unit"] = unit
        if delta is not UNSET:
            field_dict["delta"] = delta
        if tone is not UNSET:
            field_dict["tone"] = tone

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        def _parse_value(data: object) -> float | str:
            return cast(float | str, data)

        value = _parse_value(d.pop("value"))


        def _parse_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))


        def _parse_delta(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        delta = _parse_delta(d.pop("delta", UNSET))


        def _parse_tone(data: object) -> None | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItemToneType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                tone_type_0 = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItemToneType0(data)



                return tone_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTilesDataTilesItemToneType0 | Unset, data)

        tone = _parse_tone(d.pop("tone", UNSET))


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_scalar_tiles_data_tiles_item = cls(
            label=label,
            value=value,
            unit=unit,
            delta=delta,
            tone=tone,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_scalar_tiles_data_tiles_item

