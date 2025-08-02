from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateAccountJsonBody")


@_attrs_define
class CreateAccountJsonBody:
    """
    Attributes:
        expires_in (int):
        client (str):
        refresh_token (Union[Unset, str]):
        grant_type (Union[Unset, str]):  Default: 'authorization_code'.
        cc_client_id (Union[Unset, str]): OAuth client ID for resource-level credentials (client_credentials flow only)
        cc_client_secret (Union[Unset, str]): OAuth client secret for resource-level credentials (client_credentials
            flow only)
        cc_token_url (Union[Unset, str]): OAuth token URL override for resource-level authentication (client_credentials
            flow only)
    """

    expires_in: int
    client: str
    refresh_token: Union[Unset, str] = UNSET
    grant_type: Union[Unset, str] = "authorization_code"
    cc_client_id: Union[Unset, str] = UNSET
    cc_client_secret: Union[Unset, str] = UNSET
    cc_token_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        expires_in = self.expires_in
        client = self.client
        refresh_token = self.refresh_token
        grant_type = self.grant_type
        cc_client_id = self.cc_client_id
        cc_client_secret = self.cc_client_secret
        cc_token_url = self.cc_token_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expires_in": expires_in,
                "client": client,
            }
        )
        if refresh_token is not UNSET:
            field_dict["refresh_token"] = refresh_token
        if grant_type is not UNSET:
            field_dict["grant_type"] = grant_type
        if cc_client_id is not UNSET:
            field_dict["cc_client_id"] = cc_client_id
        if cc_client_secret is not UNSET:
            field_dict["cc_client_secret"] = cc_client_secret
        if cc_token_url is not UNSET:
            field_dict["cc_token_url"] = cc_token_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expires_in = d.pop("expires_in")

        client = d.pop("client")

        refresh_token = d.pop("refresh_token", UNSET)

        grant_type = d.pop("grant_type", UNSET)

        cc_client_id = d.pop("cc_client_id", UNSET)

        cc_client_secret = d.pop("cc_client_secret", UNSET)

        cc_token_url = d.pop("cc_token_url", UNSET)

        create_account_json_body = cls(
            expires_in=expires_in,
            client=client,
            refresh_token=refresh_token,
            grant_type=grant_type,
            cc_client_id=cc_client_id,
            cc_client_secret=cc_client_secret,
            cc_token_url=cc_token_url,
        )

        create_account_json_body.additional_properties = d
        return create_account_json_body

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
