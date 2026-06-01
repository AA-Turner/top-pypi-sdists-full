from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.forwarder_type_placeholder import ForwarderTypePlaceholder


T = TypeVar("T", bound="ForwarderTypeAttributesPlaceholders")


@_attrs_define
class ForwarderTypeAttributesPlaceholders:
    """UI metadata keyed by placeholder name. Each `{name}` token appearing in `configuration` (URL, header value) has a
    matching entry here describing how to prompt for it.

    """

    additional_properties: dict[str, ForwarderTypePlaceholder] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.forwarder_type_placeholder import ForwarderTypePlaceholder

        d = dict(src_dict)
        forwarder_type_attributes_placeholders = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ForwarderTypePlaceholder.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        forwarder_type_attributes_placeholders.additional_properties = additional_properties
        return forwarder_type_attributes_placeholders

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> ForwarderTypePlaceholder:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: ForwarderTypePlaceholder) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
