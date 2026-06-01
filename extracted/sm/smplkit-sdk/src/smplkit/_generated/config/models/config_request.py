from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.config_resource import ConfigResource


T = TypeVar("T", bound="ConfigRequest")


@_attrs_define
class ConfigRequest:
    """JSON:API request envelope for updating a config.

    Attributes:
        data (ConfigResource): JSON:API resource envelope for a config.

            `id` is the human-readable key for the config and must be supplied
            by the caller on create. It is unique within the account. Example: {'attributes': {'created_at':
            '2026-05-11T12:00:00Z', 'description': 'Database connection settings.', 'environments': {'prod': {'host': 'db-
            prod.internal'}}, 'items': {'host': {'description': 'Primary database hostname.', 'type': 'STRING', 'value':
            'db.internal'}}, 'name': 'Database', 'parent': 'common', 'updated_at': '2026-05-11T12:00:00Z'}, 'id':
            'database', 'type': 'config'}.
    """

    data: ConfigResource
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
        from ..models.config_resource import ConfigResource

        d = dict(src_dict)
        data = ConfigResource.from_dict(d.pop("data"))

        config_request = cls(
            data=data,
        )

        config_request.additional_properties = d
        return config_request

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
