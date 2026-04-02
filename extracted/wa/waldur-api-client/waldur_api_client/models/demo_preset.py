from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.demo_preset_entity_counts import DemoPresetEntityCounts


T = TypeVar("T", bound="DemoPreset")


@_attrs_define
class DemoPreset:
    """
    Attributes:
        name (str):
        title (str):
        description (str):
        version (str):
        entity_counts (DemoPresetEntityCounts):
        scenarios (list[str]):
    """

    name: str
    title: str
    description: str
    version: str
    entity_counts: "DemoPresetEntityCounts"
    scenarios: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        title = self.title

        description = self.description

        version = self.version

        entity_counts = self.entity_counts.to_dict()

        scenarios = self.scenarios

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "title": title,
                "description": description,
                "version": version,
                "entity_counts": entity_counts,
                "scenarios": scenarios,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.demo_preset_entity_counts import DemoPresetEntityCounts

        d = dict(src_dict)
        name = d.pop("name")

        title = d.pop("title")

        description = d.pop("description")

        version = d.pop("version")

        entity_counts = DemoPresetEntityCounts.from_dict(d.pop("entity_counts"))

        scenarios = cast(list[str], d.pop("scenarios"))

        demo_preset = cls(
            name=name,
            title=title,
            description=description,
            version=version,
            entity_counts=entity_counts,
            scenarios=scenarios,
        )

        demo_preset.additional_properties = d
        return demo_preset

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
