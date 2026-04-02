from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Saml2LogoutComplete")


@_attrs_define
class Saml2LogoutComplete:
    """
    Attributes:
        saml_response (Union[Unset, str]):
        saml_request (Union[Unset, str]):
    """

    saml_response: Union[Unset, str] = UNSET
    saml_request: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        saml_response = self.saml_response

        saml_request = self.saml_request

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if saml_response is not UNSET:
            field_dict["SAMLResponse"] = saml_response
        if saml_request is not UNSET:
            field_dict["SAMLRequest"] = saml_request

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        saml_response = d.pop("SAMLResponse", UNSET)

        saml_request = d.pop("SAMLRequest", UNSET)

        saml_2_logout_complete = cls(
            saml_response=saml_response,
            saml_request=saml_request,
        )

        saml_2_logout_complete.additional_properties = d
        return saml_2_logout_complete

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
