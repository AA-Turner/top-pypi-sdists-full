from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.api_key_resource import ApiKeyResource


T = TypeVar("T", bound="ApiKeyRequest")


@_attrs_define
class ApiKeyRequest:
    """JSON:API request envelope for creating or updating an API key.

    Attributes:
        data (ApiKeyResource): JSON:API resource envelope for an API key.

            `id` must not be specified for create requests (the server assigns it). Example: {'attributes': {'created_at':
            '2026-03-20T11:02:16.616Z', 'created_by': 'd290f1ee-6c54-4b01-90e6-d701748f0851', 'expires_at':
            '2027-03-20T11:02:16.616Z', 'key': 'sk_api_a1b2c3d4e5f6g7h8i9j0', 'last_used_at': '2026-03-19T08:45:00.000Z',
            'name': 'Production API Key', 'scopes': {}, 'status': 'ACTIVE', 'updated_at': '2026-03-20T11:02:16.616Z'}, 'id':
            'b2c3d4e5-f6a7-8901-bcde-f12345678901', 'type': 'api_key'}.
    """

    data: ApiKeyResource
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
        from ..models.api_key_resource import ApiKeyResource

        d = dict(src_dict)
        data = ApiKeyResource.from_dict(d.pop("data"))

        api_key_request = cls(
            data=data,
        )

        api_key_request.additional_properties = d
        return api_key_request

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
