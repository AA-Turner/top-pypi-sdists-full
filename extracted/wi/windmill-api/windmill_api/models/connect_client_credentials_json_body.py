from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConnectClientCredentialsJsonBody")


@_attrs_define
class ConnectClientCredentialsJsonBody:
    """
    Attributes:
        scopes (Union[Unset, List[str]]):
        cc_client_id (Union[Unset, str]): OAuth client ID. Omit to use the credentials configured on the provider's
            instance OAuth entry.
        cc_client_secret (Union[Unset, str]): OAuth client secret. Omit to use the credentials configured on the
            provider's instance OAuth entry.
        cc_instance (Union[Unset, str]): Instance name for built-in providers whose client-credentials token URL is
            instance-templated; substituted into the fixed-host registry template server-side. The token URL is never
            caller-supplied.
    """

    scopes: Union[Unset, List[str]] = UNSET
    cc_client_id: Union[Unset, str] = UNSET
    cc_client_secret: Union[Unset, str] = UNSET
    cc_instance: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scopes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        cc_client_id = self.cc_client_id
        cc_client_secret = self.cc_client_secret
        cc_instance = self.cc_instance

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if cc_client_id is not UNSET:
            field_dict["cc_client_id"] = cc_client_id
        if cc_client_secret is not UNSET:
            field_dict["cc_client_secret"] = cc_client_secret
        if cc_instance is not UNSET:
            field_dict["cc_instance"] = cc_instance

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        scopes = cast(List[str], d.pop("scopes", UNSET))

        cc_client_id = d.pop("cc_client_id", UNSET)

        cc_client_secret = d.pop("cc_client_secret", UNSET)

        cc_instance = d.pop("cc_instance", UNSET)

        connect_client_credentials_json_body = cls(
            scopes=scopes,
            cc_client_id=cc_client_id,
            cc_client_secret=cc_client_secret,
            cc_instance=cc_instance,
        )

        connect_client_credentials_json_body.additional_properties = d
        return connect_client_credentials_json_body

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
