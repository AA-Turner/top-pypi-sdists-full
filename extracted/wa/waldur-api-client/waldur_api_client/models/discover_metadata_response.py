from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.discover_metadata_response_endpoints import DiscoverMetadataResponseEndpoints
    from ..models.waldur_field_suggestion import WaldurFieldSuggestion


T = TypeVar("T", bound="DiscoverMetadataResponse")


@_attrs_define
class DiscoverMetadataResponse:
    """
    Attributes:
        claims_supported (list[str]): List of claims supported by the OIDC provider
        scopes_supported (list[str]): List of scopes supported by the OIDC provider
        endpoints (DiscoverMetadataResponseEndpoints): OIDC endpoints (authorization, token, userinfo, logout)
        waldur_fields (list['WaldurFieldSuggestion']): Waldur User fields with suggested OIDC claim mappings
        suggested_scopes (list[str]): Recommended scopes to request based on claim mappings
    """

    claims_supported: list[str]
    scopes_supported: list[str]
    endpoints: "DiscoverMetadataResponseEndpoints"
    waldur_fields: list["WaldurFieldSuggestion"]
    suggested_scopes: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        claims_supported = self.claims_supported

        scopes_supported = self.scopes_supported

        endpoints = self.endpoints.to_dict()

        waldur_fields = []
        for waldur_fields_item_data in self.waldur_fields:
            waldur_fields_item = waldur_fields_item_data.to_dict()
            waldur_fields.append(waldur_fields_item)

        suggested_scopes = self.suggested_scopes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "claims_supported": claims_supported,
                "scopes_supported": scopes_supported,
                "endpoints": endpoints,
                "waldur_fields": waldur_fields,
                "suggested_scopes": suggested_scopes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.discover_metadata_response_endpoints import DiscoverMetadataResponseEndpoints
        from ..models.waldur_field_suggestion import WaldurFieldSuggestion

        d = dict(src_dict)
        claims_supported = cast(list[str], d.pop("claims_supported"))

        scopes_supported = cast(list[str], d.pop("scopes_supported"))

        endpoints = DiscoverMetadataResponseEndpoints.from_dict(d.pop("endpoints"))

        waldur_fields = []
        _waldur_fields = d.pop("waldur_fields")
        for waldur_fields_item_data in _waldur_fields:
            waldur_fields_item = WaldurFieldSuggestion.from_dict(waldur_fields_item_data)

            waldur_fields.append(waldur_fields_item)

        suggested_scopes = cast(list[str], d.pop("suggested_scopes"))

        discover_metadata_response = cls(
            claims_supported=claims_supported,
            scopes_supported=scopes_supported,
            endpoints=endpoints,
            waldur_fields=waldur_fields,
            suggested_scopes=suggested_scopes,
        )

        discover_metadata_response.additional_properties = d
        return discover_metadata_response

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
