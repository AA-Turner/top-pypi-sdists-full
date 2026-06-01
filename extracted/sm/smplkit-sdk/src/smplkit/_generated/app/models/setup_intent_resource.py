from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.setup_intent_resource_type import check_setup_intent_resource_type
from ..models.setup_intent_resource_type import SetupIntentResourceType

if TYPE_CHECKING:
    from ..models.setup_intent_attributes import SetupIntentAttributes


T = TypeVar("T", bound="SetupIntentResource")


@_attrs_define
class SetupIntentResource:
    """
    Example:
        {'attributes': {'client_secret': 'seti_1234567890abcdef_secret_xyz'}, 'type': 'setup_intent'}

    Attributes:
        type_ (SetupIntentResourceType):
        attributes (SetupIntentAttributes): Result of executing the setup-intent function.
    """

    type_: SetupIntentResourceType
    attributes: SetupIntentAttributes
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.setup_intent_attributes import SetupIntentAttributes

        d = dict(src_dict)
        type_ = check_setup_intent_resource_type(d.pop("type"))

        attributes = SetupIntentAttributes.from_dict(d.pop("attributes"))

        setup_intent_resource = cls(
            type_=type_,
            attributes=attributes,
        )

        setup_intent_resource.additional_properties = d
        return setup_intent_resource

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
