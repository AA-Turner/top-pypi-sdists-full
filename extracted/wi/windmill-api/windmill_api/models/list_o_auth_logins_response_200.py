from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_o_auth_logins_response_200_oauth_item import ListOAuthLoginsResponse200OauthItem


T = TypeVar("T", bound="ListOAuthLoginsResponse200")


@_attrs_define
class ListOAuthLoginsResponse200:
    """
    Attributes:
        oauth (List['ListOAuthLoginsResponse200OauthItem']):
        saml (Union[Unset, str]):
    """

    oauth: List["ListOAuthLoginsResponse200OauthItem"]
    saml: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        oauth = []
        for oauth_item_data in self.oauth:
            oauth_item = oauth_item_data.to_dict()

            oauth.append(oauth_item)

        saml = self.saml

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "oauth": oauth,
            }
        )
        if saml is not UNSET:
            field_dict["saml"] = saml

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_o_auth_logins_response_200_oauth_item import ListOAuthLoginsResponse200OauthItem

        d = src_dict.copy()
        oauth = []
        _oauth = d.pop("oauth")
        for oauth_item_data in _oauth:
            oauth_item = ListOAuthLoginsResponse200OauthItem.from_dict(oauth_item_data)

            oauth.append(oauth_item)

        saml = d.pop("saml", UNSET)

        list_o_auth_logins_response_200 = cls(
            oauth=oauth,
            saml=saml,
        )

        list_o_auth_logins_response_200.additional_properties = d
        return list_o_auth_logins_response_200

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
