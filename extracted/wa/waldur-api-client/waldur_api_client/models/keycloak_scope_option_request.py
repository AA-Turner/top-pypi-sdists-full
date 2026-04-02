from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="KeycloakScopeOptionRequest")


@_attrs_define
class KeycloakScopeOptionRequest:
    """
    Attributes:
        scope_type (str): Scope type, e.g. 'project', 'cluster'.
        scope_id (str): Identifier of the scope (UUID or external ID).
        label (str): Human-readable label shown to end users.
    """

    scope_type: str
    scope_id: str
    label: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope_type = self.scope_type

        scope_id = self.scope_id

        label = self.label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope_type": scope_type,
                "scope_id": scope_id,
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scope_type = d.pop("scope_type")

        scope_id = d.pop("scope_id")

        label = d.pop("label")

        keycloak_scope_option_request = cls(
            scope_type=scope_type,
            scope_id=scope_id,
            label=label,
        )

        keycloak_scope_option_request.additional_properties = d
        return keycloak_scope_option_request

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
