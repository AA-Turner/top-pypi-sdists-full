from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast
from typing import Literal

if TYPE_CHECKING:
    from ..models.flag import Flag


T = TypeVar("T", bound="FlagCreateResource")


@_attrs_define
class FlagCreateResource:
    """JSON:API resource envelope for creating a flag (id required).

    Example:
        {'attributes': {'default': False, 'description': 'Enable the redesigned checkout flow.', 'name': 'Checkout V2',
            'type': 'BOOLEAN'}, 'id': 'checkout-v2', 'type': 'flag'}

    Attributes:
        id (str): Client-supplied resource id.
        type_ (Literal['flag']):
        attributes (Flag): A feature flag whose value is resolved at runtime from environment
            rules and a default.

            A flag has a value type (`BOOLEAN`, `STRING`, `NUMERIC`, or `JSON`)
            and either a fixed set of allowed values (constrained) or accepts
            any value matching the type (unconstrained). Each environment can
            enable or disable the flag, set its own default, and define
            targeting rules that override the default for specific evaluation
            contexts. Example: {'created_at': '2026-03-27T10:00:00Z', 'default': False, 'description': 'Enable dark mode for
            the application UI', 'environments': {'production': {'default': False, 'enabled': True, 'rules':
            [{'description': 'Beta users get dark mode', 'logic': {'==': [{'var': 'customer.beta'}, True]}, 'value':
            True}]}, 'staging': {'default': True, 'enabled': True, 'rules': []}}, 'managed': True, 'name': 'Dark Mode',
            'type': 'BOOLEAN', 'updated_at': '2026-03-27T10:00:00Z', 'values': [{'name': 'on', 'value': True}, {'name':
            'off', 'value': False}]}.
    """

    id: str
    type_: Literal["flag"]
    attributes: Flag
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flag import Flag

        d = dict(src_dict)
        id = d.pop("id")

        type_ = cast(Literal["flag"], d.pop("type"))
        if type_ != "flag":
            raise ValueError(f"type must match const 'flag', got '{type_}'")

        attributes = Flag.from_dict(d.pop("attributes"))

        flag_create_resource = cls(
            id=id,
            type_=type_,
            attributes=attributes,
        )

        flag_create_resource.additional_properties = d
        return flag_create_resource

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
