from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.flag_resource import FlagResource


T = TypeVar("T", bound="FlagRequest")


@_attrs_define
class FlagRequest:
    """JSON:API request envelope for updating a flag.

    Attributes:
        data (FlagResource): JSON:API resource envelope for a flag.

            `id` is the flag key. For create requests, `id` is required and is
            chosen by the caller. For update requests, `id` may be omitted (the
            server reads the key from the URL) or supplied to rename the flag. Example: {'attributes': {'created_at':
            '2026-03-27T10:00:00Z', 'default': False, 'description': 'Enable dark mode for the application UI',
            'environments': {'production': {'default': False, 'enabled': True, 'rules': [{'description': 'Beta users get
            dark mode', 'logic': {'==': [{'var': 'customer.beta'}, True]}, 'value': True}]}}, 'managed': True, 'name': 'Dark
            Mode', 'type': 'BOOLEAN', 'updated_at': '2026-03-27T10:00:00Z', 'values': [{'name': 'on', 'value': True},
            {'name': 'off', 'value': False}]}, 'id': 'dark-mode', 'type': 'flag'}.
    """

    data: FlagResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flag_resource import FlagResource

        d = dict(src_dict)
        data = FlagResource.from_dict(d.pop("data"))

        flag_request = cls(
            data=data,
        )

        flag_request.additional_properties = d
        return flag_request

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
