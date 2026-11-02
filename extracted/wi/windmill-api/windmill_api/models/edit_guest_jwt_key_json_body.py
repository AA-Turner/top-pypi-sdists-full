from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditGuestJwtKeyJsonBody")


@_attrs_define
class EditGuestJwtKeyJsonBody:
    """
    Attributes:
        public_key (Union[Unset, str]): A PEM public key (RS or ES family).
        jwks_url (Union[Unset, str]): A JWKS URL whose keys are fetched and refreshed.
    """

    public_key: Union[Unset, str] = UNSET
    jwks_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        public_key = self.public_key
        jwks_url = self.jwks_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if public_key is not UNSET:
            field_dict["public_key"] = public_key
        if jwks_url is not UNSET:
            field_dict["jwks_url"] = jwks_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        public_key = d.pop("public_key", UNSET)

        jwks_url = d.pop("jwks_url", UNSET)

        edit_guest_jwt_key_json_body = cls(
            public_key=public_key,
            jwks_url=jwks_url,
        )

        edit_guest_jwt_key_json_body.additional_properties = d
        return edit_guest_jwt_key_json_body

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
