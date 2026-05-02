from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkspaceOAuthConfig")


@_attrs_define
class WorkspaceOAuthConfig:
    """
    Attributes:
        client_id (str): The OAuth client ID for the workspace
        client_secret (str): The OAuth client secret for the workspace
        base_url (str): The base URL of the workspace
        redirect_uri (str): The OAuth redirect URI
    """

    client_id: str
    client_secret: str
    base_url: str
    redirect_uri: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        client_id = self.client_id
        client_secret = self.client_secret
        base_url = self.base_url
        redirect_uri = self.redirect_uri

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "base_url": base_url,
                "redirect_uri": redirect_uri,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        client_id = d.pop("client_id")

        client_secret = d.pop("client_secret")

        base_url = d.pop("base_url")

        redirect_uri = d.pop("redirect_uri")

        workspace_o_auth_config = cls(
            client_id=client_id,
            client_secret=client_secret,
            base_url=base_url,
            redirect_uri=redirect_uri,
        )

        workspace_o_auth_config.additional_properties = d
        return workspace_o_auth_config

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
