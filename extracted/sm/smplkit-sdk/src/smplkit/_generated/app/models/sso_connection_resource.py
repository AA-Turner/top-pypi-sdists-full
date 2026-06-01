from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sso_connection_resource_type import check_sso_connection_resource_type
from ..models.sso_connection_resource_type import SSOConnectionResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.sso_connection import SSOConnection


T = TypeVar("T", bound="SSOConnectionResource")


@_attrs_define
class SSOConnectionResource:
    """JSON:API resource envelope for an SSO connection.

    `id` is the server-assigned UUID of the singleton connection row on
    the account; clients never specify it (the URL is
    `/accounts/current/sso_connection` with no id segment).

        Example:
            {'attributes': {'acs_url': 'https://app.smplkit.com/api/v1/auth/sso/acs', 'created_at':
                '2026-05-25T11:02:16.616Z', 'default_role': 'MEMBER', 'enforced': True, 'group_role_mappings': {'smplkit-
                admins': 'ADMIN'}, 'oidc_client_id': 'smplkit-acme', 'oidc_issuer': 'https://login.acme.com', 'protocol':
                'oidc', 'slo_url': 'https://app.smplkit.com/api/v1/auth/sso/slo', 'sp_entity_id':
                'https://app.smplkit.com/sso/sp', 'updated_at': '2026-05-25T11:02:16.616Z'}, 'id': 'c0ffee01-1234-5678-9abc-
                def012345678', 'type': 'sso_connection'}

        Attributes:
            type_ (SSOConnectionResourceType):
            attributes (SSOConnection): An account's Single Sign-On connection to a customer-controlled
                identity provider. Configuring a connection lets the account federate
                authentication to its own SAML or OIDC IdP; with `enforced` enabled,
                password and social sign-in are disabled for users on the account's
                verified domains.

                Each account has at most one SSO connection. The Service Provider
                metadata fields (`sp_entity_id`, `acs_url`, `slo_url`) are computed
                on every read from the connection identifier and never stored. Example: {'acs_url':
                'https://app.smplkit.com/api/v1/auth/sso/acs', 'created_at': '2026-05-25T11:02:16.616Z', 'default_role':
                'MEMBER', 'enforced': True, 'group_role_mappings': {'smplkit-admins': 'ADMIN'}, 'oidc_client_id': 'smplkit-
                acme', 'oidc_issuer': 'https://login.acme.com', 'protocol': 'oidc', 'slo_url':
                'https://app.smplkit.com/api/v1/auth/sso/slo', 'sp_entity_id': 'https://app.smplkit.com/sso/sp', 'updated_at':
                '2026-05-25T11:02:16.616Z'}.
            id (None | str | Unset):
    """

    type_: SSOConnectionResourceType
    attributes: SSOConnection
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
        from ..models.sso_connection import SSOConnection

        d = dict(src_dict)
        type_ = check_sso_connection_resource_type(d.pop("type"))

        attributes = SSOConnection.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        sso_connection_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        sso_connection_resource.additional_properties = d
        return sso_connection_resource

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
