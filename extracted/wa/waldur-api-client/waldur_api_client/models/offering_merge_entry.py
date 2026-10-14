from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.offering_merge_area_enum import OfferingMergeAreaEnum
from ..models.offering_merge_effect_enum import OfferingMergeEffectEnum

T = TypeVar("T", bound="OfferingMergeEntry")


@_attrs_define
class OfferingMergeEntry:
    """
    Attributes:
        label (str): Coverage registry entry, as model.Field label.
        area (OfferingMergeAreaEnum):
        area_title (str): The area, for a human reader.
        effect (OfferingMergeEffectEnum):
        effect_title (str): The effect, for a human reader.
        count (int): Rows the entry covers.
        left_on_source (int): Of those, rows that stay on a source because the target has them already.
        can_list_rows (bool): Whether the affected endpoint can list the rows one by one.
    """

    label: str
    area: OfferingMergeAreaEnum
    area_title: str
    effect: OfferingMergeEffectEnum
    effect_title: str
    count: int
    left_on_source: int
    can_list_rows: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        area = self.area.value

        area_title = self.area_title

        effect = self.effect.value

        effect_title = self.effect_title

        count = self.count

        left_on_source = self.left_on_source

        can_list_rows = self.can_list_rows

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
                "area": area,
                "area_title": area_title,
                "effect": effect,
                "effect_title": effect_title,
                "count": count,
                "left_on_source": left_on_source,
                "can_list_rows": can_list_rows,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        area = OfferingMergeAreaEnum(d.pop("area"))

        area_title = d.pop("area_title")

        effect = OfferingMergeEffectEnum(d.pop("effect"))

        effect_title = d.pop("effect_title")

        count = d.pop("count")

        left_on_source = d.pop("left_on_source")

        can_list_rows = d.pop("can_list_rows")

        offering_merge_entry = cls(
            label=label,
            area=area,
            area_title=area_title,
            effect=effect,
            effect_title=effect_title,
            count=count,
            left_on_source=left_on_source,
            can_list_rows=can_list_rows,
        )

        offering_merge_entry.additional_properties = d
        return offering_merge_entry

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
