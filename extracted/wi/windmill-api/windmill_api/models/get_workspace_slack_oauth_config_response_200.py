from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetWorkspaceSlackOauthConfigResponse200")


@_attrs_define
class GetWorkspaceSlackOauthConfigResponse200:
    """
    Attributes:
        slack_oauth_client_id (Union[Unset, None, str]):
        slack_oauth_client_secret (Union[Unset, None, str]): Masked with *** if set
    """

    slack_oauth_client_id: Union[Unset, None, str] = UNSET
    slack_oauth_client_secret: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        slack_oauth_client_id = self.slack_oauth_client_id
        slack_oauth_client_secret = self.slack_oauth_client_secret

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if slack_oauth_client_id is not UNSET:
            field_dict["slack_oauth_client_id"] = slack_oauth_client_id
        if slack_oauth_client_secret is not UNSET:
            field_dict["slack_oauth_client_secret"] = slack_oauth_client_secret

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        slack_oauth_client_id = d.pop("slack_oauth_client_id", UNSET)

        slack_oauth_client_secret = d.pop("slack_oauth_client_secret", UNSET)

        get_workspace_slack_oauth_config_response_200 = cls(
            slack_oauth_client_id=slack_oauth_client_id,
            slack_oauth_client_secret=slack_oauth_client_secret,
        )

        get_workspace_slack_oauth_config_response_200.additional_properties = d
        return get_workspace_slack_oauth_config_response_200

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
