from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Literal

if TYPE_CHECKING:
    from ..models.flag import Flag


T = TypeVar("T", bound="FlagResource")


@_attrs_define
class FlagResource:
    """JSON:API resource envelope for a flag.

    `id` is the flag key. For create requests, `id` is required and is
    chosen by the caller. For update requests, `id` may be omitted (the
    server reads the key from the URL) or supplied to rename the flag.

        Example:
            {'attributes': {'created_at': '2026-03-27T10:00:00Z', 'default': False, 'description': 'Enable dark mode for the
                application UI', 'environments': {'production': {'default': False, 'enabled': True, 'rules': [{'description':
                'Beta users get dark mode', 'logic': {'==': [{'var': 'customer.beta'}, True]}, 'value': True}]}}, 'managed':
                True, 'name': 'Dark Mode', 'type': 'BOOLEAN', 'updated_at': '2026-03-27T10:00:00Z', 'values': [{'name': 'on',
                'value': True}, {'name': 'off', 'value': False}]}, 'id': 'dark-mode', 'type': 'flag'}

        Attributes:
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
            id (None | str | Unset):
    """

    type_: Literal["flag"]
    attributes: Flag
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flag import Flag

        d = dict(src_dict)
        type_ = cast(Literal["flag"], d.pop("type"))
        if type_ != "flag":
            raise ValueError(f"type must match const 'flag', got '{type_}'")

        attributes = Flag.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        flag_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        flag_resource.additional_properties = d
        return flag_resource

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
