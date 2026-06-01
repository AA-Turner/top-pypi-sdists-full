from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.api_key_resource_type import ApiKeyResourceType
from ..models.api_key_resource_type import check_api_key_resource_type
from typing import cast

if TYPE_CHECKING:
    from ..models.api_key import ApiKey


T = TypeVar("T", bound="ApiKeyResource")


@_attrs_define
class ApiKeyResource:
    """JSON:API resource envelope for an API key.

    `id` must not be specified for create requests (the server assigns it).

        Example:
            {'attributes': {'created_at': '2026-03-20T11:02:16.616Z', 'created_by': 'd290f1ee-6c54-4b01-90e6-d701748f0851',
                'expires_at': '2027-03-20T11:02:16.616Z', 'key': 'sk_api_a1b2c3d4e5f6g7h8i9j0', 'last_used_at':
                '2026-03-19T08:45:00.000Z', 'name': 'Production API Key', 'scopes': {}, 'status': 'ACTIVE', 'updated_at':
                '2026-03-20T11:02:16.616Z'}, 'id': 'b2c3d4e5-f6a7-8901-bcde-f12345678901', 'type': 'api_key'}

        Attributes:
            type_ (ApiKeyResourceType):
            attributes (ApiKey): An API key used by SDKs, scripts, and other programmatic clients to
                authenticate with the smplkit API on behalf of the account.

                The full key value is returned in plaintext on the create response and
                is otherwise unavailable — record it somewhere safe immediately after
                creation. Example: {'created_at': '2026-03-20T11:02:16.616Z', 'created_by':
                'd290f1ee-6c54-4b01-90e6-d701748f0851', 'expires_at': '2027-03-20T11:02:16.616Z', 'key':
                'sk_api_a1b2c3d4e5f6g7h8i9j0', 'last_used_at': '2026-03-19T08:45:00.000Z', 'name': 'Production API Key',
                'scopes': {}, 'status': 'ACTIVE', 'updated_at': '2026-03-20T11:02:16.616Z'}.
            id (None | str | Unset):
    """

    type_: ApiKeyResourceType
    attributes: ApiKey
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

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
        from ..models.api_key import ApiKey

        d = dict(src_dict)
        type_ = check_api_key_resource_type(d.pop("type"))

        attributes = ApiKey.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        api_key_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        api_key_resource.additional_properties = d
        return api_key_resource

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
