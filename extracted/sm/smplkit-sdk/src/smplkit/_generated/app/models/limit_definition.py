from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="LimitDefinition")


@_attrs_define
class LimitDefinition:
    """Description of a single metered limit on a product.

    Attributes:
        display_name (str): Human-readable name for the limit.
        description (str): Long-form description of what the limit controls.
        unit (str): Unit the limit is measured in, e.g. `flags`, `events`.
        display_format (None | str | Unset): Optional formatter hint for rendering the limit value in customer-facing
            UI.
    """

    display_name: str
    description: str
    unit: str
    display_format: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        description = self.description

        unit = self.unit

        display_format: None | str | Unset
        if isinstance(self.display_format, Unset):
            display_format = UNSET
        else:
            display_format = self.display_format

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "display_name": display_name,
                "description": description,
                "unit": unit,
            }
        )
        if display_format is not UNSET:
            field_dict["display_format"] = display_format

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        display_name = d.pop("display_name")

        description = d.pop("description")

        unit = d.pop("unit")

        def _parse_display_format(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        display_format = _parse_display_format(d.pop("display_format", UNSET))

        limit_definition = cls(
            display_name=display_name,
            description=description,
            unit=unit,
            display_format=display_format,
        )

        limit_definition.additional_properties = d
        return limit_definition

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
