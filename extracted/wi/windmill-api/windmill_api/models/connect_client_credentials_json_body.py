from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConnectClientCredentialsJsonBody")


@_attrs_define
class ConnectClientCredentialsJsonBody:
    """
    Attributes:
        cc_client_id (str): OAuth client ID for resource-level authentication
        cc_client_secret (str): OAuth client secret for resource-level authentication
        scopes (Union[Unset, List[str]]):
        cc_token_url (Union[Unset, str]): OAuth token URL override for resource-level authentication
    """

    cc_client_id: str
    cc_client_secret: str
    scopes: Union[Unset, List[str]] = UNSET
    cc_token_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cc_client_id = self.cc_client_id
        cc_client_secret = self.cc_client_secret
        scopes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        cc_token_url = self.cc_token_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cc_client_id": cc_client_id,
                "cc_client_secret": cc_client_secret,
            }
        )
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if cc_token_url is not UNSET:
            field_dict["cc_token_url"] = cc_token_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cc_client_id = d.pop("cc_client_id")

        cc_client_secret = d.pop("cc_client_secret")

        scopes = cast(List[str], d.pop("scopes", UNSET))

        cc_token_url = d.pop("cc_token_url", UNSET)

        connect_client_credentials_json_body = cls(
            cc_client_id=cc_client_id,
            cc_client_secret=cc_client_secret,
            scopes=scopes,
            cc_token_url=cc_token_url,
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
