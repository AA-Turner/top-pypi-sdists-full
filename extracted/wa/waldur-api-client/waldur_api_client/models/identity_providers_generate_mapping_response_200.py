from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.identity_providers_generate_mapping_response_200_attribute_mapping import (
        IdentityProvidersGenerateMappingResponse200AttributeMapping,
    )


T = TypeVar("T", bound="IdentityProvidersGenerateMappingResponse200")


@_attrs_define
class IdentityProvidersGenerateMappingResponse200:
    """
    Attributes:
        attribute_mapping (Union[Unset, IdentityProvidersGenerateMappingResponse200AttributeMapping]): Suggested mapping
            of Waldur fields to OIDC claims
        extra_scope (Union[Unset, str]): Suggested scopes to request (space-separated)
    """

    attribute_mapping: Union[Unset, "IdentityProvidersGenerateMappingResponse200AttributeMapping"] = UNSET
    extra_scope: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attribute_mapping: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attribute_mapping, Unset):
            attribute_mapping = self.attribute_mapping.to_dict()

        extra_scope = self.extra_scope

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attribute_mapping is not UNSET:
            field_dict["attribute_mapping"] = attribute_mapping
        if extra_scope is not UNSET:
            field_dict["extra_scope"] = extra_scope

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.identity_providers_generate_mapping_response_200_attribute_mapping import (
            IdentityProvidersGenerateMappingResponse200AttributeMapping,
        )

        d = dict(src_dict)
        _attribute_mapping = d.pop("attribute_mapping", UNSET)
        attribute_mapping: Union[Unset, IdentityProvidersGenerateMappingResponse200AttributeMapping]
        if isinstance(_attribute_mapping, Unset):
            attribute_mapping = UNSET
        else:
            attribute_mapping = IdentityProvidersGenerateMappingResponse200AttributeMapping.from_dict(
                _attribute_mapping
            )

        extra_scope = d.pop("extra_scope", UNSET)

        identity_providers_generate_mapping_response_200 = cls(
            attribute_mapping=attribute_mapping,
            extra_scope=extra_scope,
        )

        identity_providers_generate_mapping_response_200.additional_properties = d
        return identity_providers_generate_mapping_response_200

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
