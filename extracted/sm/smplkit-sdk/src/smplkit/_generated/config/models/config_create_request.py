from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.config_create_resource import ConfigCreateResource


T = TypeVar("T", bound="ConfigCreateRequest")


@_attrs_define
class ConfigCreateRequest:
    """JSON:API request envelope for creating a config.

    Distinct from :class:`ConfigRequest` because create requires
    caller-supplied ``data.id`` while update does not.

        Attributes:
            data (ConfigCreateResource): JSON:API resource envelope for creating a config (id required). Example:
                {'attributes': {'description': 'Settings for the user service.', 'environments': {'prod': {'host': 'db-
                prod.internal'}}, 'items': {'host': {'description': 'Database host.', 'type': 'STRING', 'value':
                'db.internal'}}, 'name': 'User Service', 'parent': 'common'}, 'id': 'user-service', 'type': 'config'}.
    """

    data: ConfigCreateResource
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
        from ..models.config_create_resource import ConfigCreateResource

        d = dict(src_dict)
        data = ConfigCreateResource.from_dict(d.pop("data"))

        config_create_request = cls(
            data=data,
        )

        config_create_request.additional_properties = d
        return config_create_request

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
