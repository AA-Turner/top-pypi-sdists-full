from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_credential_origin_response_200_origin import GetCredentialOriginResponse200Origin
from ..models.get_credential_origin_response_200_provider import GetCredentialOriginResponse200Provider
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetCredentialOriginResponse200")


@_attrs_define
class GetCredentialOriginResponse200:
    """
    Attributes:
        origin (Union[Unset, GetCredentialOriginResponse200Origin]):
        provider (Union[Unset, GetCredentialOriginResponse200Provider]):
    """

    origin: Union[Unset, GetCredentialOriginResponse200Origin] = UNSET
    provider: Union[Unset, GetCredentialOriginResponse200Provider] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        origin: Union[Unset, str] = UNSET
        if not isinstance(self.origin, Unset):
            origin = self.origin.value

        provider: Union[Unset, str] = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if origin is not UNSET:
            field_dict["origin"] = origin
        if provider is not UNSET:
            field_dict["provider"] = provider

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _origin = d.pop("origin", UNSET)
        origin: Union[Unset, GetCredentialOriginResponse200Origin]
        if isinstance(_origin, Unset):
            origin = UNSET
        else:
            origin = GetCredentialOriginResponse200Origin(_origin)

        _provider = d.pop("provider", UNSET)
        provider: Union[Unset, GetCredentialOriginResponse200Provider]
        if isinstance(_provider, Unset):
            provider = UNSET
        else:
            provider = GetCredentialOriginResponse200Provider(_provider)

        get_credential_origin_response_200 = cls(
            origin=origin,
            provider=provider,
        )

        get_credential_origin_response_200.additional_properties = d
        return get_credential_origin_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
