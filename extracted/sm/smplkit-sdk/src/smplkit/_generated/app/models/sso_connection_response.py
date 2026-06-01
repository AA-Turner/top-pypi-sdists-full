from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.sso_connection_resource import SSOConnectionResource


T = TypeVar("T", bound="SSOConnectionResponse")


@_attrs_define
class SSOConnectionResponse:
    """JSON:API single-resource response envelope for the SSO connection.

    Attributes:
        data (SSOConnectionResource): JSON:API resource envelope for an SSO connection.

            `id` is the server-assigned UUID of the singleton connection row on
            the account; clients never specify it (the URL is
            `/accounts/current/sso_connection` with no id segment). Example: {'attributes': {'acs_url':
            'https://app.smplkit.com/api/v1/auth/sso/acs', 'created_at': '2026-05-25T11:02:16.616Z', 'default_role':
            'MEMBER', 'enforced': True, 'group_role_mappings': {'smplkit-admins': 'ADMIN'}, 'oidc_client_id': 'smplkit-
            acme', 'oidc_issuer': 'https://login.acme.com', 'protocol': 'oidc', 'slo_url':
            'https://app.smplkit.com/api/v1/auth/sso/slo', 'sp_entity_id': 'https://app.smplkit.com/sso/sp', 'updated_at':
            '2026-05-25T11:02:16.616Z'}, 'id': 'c0ffee01-1234-5678-9abc-def012345678', 'type': 'sso_connection'}.
    """

    data: SSOConnectionResource
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
        from ..models.sso_connection_resource import SSOConnectionResource

        d = dict(src_dict)
        data = SSOConnectionResource.from_dict(d.pop("data"))

        sso_connection_response = cls(
            data=data,
        )

        sso_connection_response.additional_properties = d
        return sso_connection_response

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
