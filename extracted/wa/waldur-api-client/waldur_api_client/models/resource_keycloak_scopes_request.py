from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.keycloak_scope_option_request import KeycloakScopeOptionRequest


T = TypeVar("T", bound="ResourceKeycloakScopesRequest")


@_attrs_define
class ResourceKeycloakScopesRequest:
    """
    Attributes:
        keycloak_available_scopes (list['KeycloakScopeOptionRequest']): Pre-configured scope options for this resource.
    """

    keycloak_available_scopes: list["KeycloakScopeOptionRequest"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        keycloak_available_scopes = []
        for keycloak_available_scopes_item_data in self.keycloak_available_scopes:
            keycloak_available_scopes_item = keycloak_available_scopes_item_data.to_dict()
            keycloak_available_scopes.append(keycloak_available_scopes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "keycloak_available_scopes": keycloak_available_scopes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.keycloak_scope_option_request import KeycloakScopeOptionRequest

        d = dict(src_dict)
        keycloak_available_scopes = []
        _keycloak_available_scopes = d.pop("keycloak_available_scopes")
        for keycloak_available_scopes_item_data in _keycloak_available_scopes:
            keycloak_available_scopes_item = KeycloakScopeOptionRequest.from_dict(keycloak_available_scopes_item_data)

            keycloak_available_scopes.append(keycloak_available_scopes_item)

        resource_keycloak_scopes_request = cls(
            keycloak_available_scopes=keycloak_available_scopes,
        )

        resource_keycloak_scopes_request.additional_properties = d
        return resource_keycloak_scopes_request

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
