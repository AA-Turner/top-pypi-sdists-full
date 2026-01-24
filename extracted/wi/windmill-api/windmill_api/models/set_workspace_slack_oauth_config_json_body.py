from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SetWorkspaceSlackOauthConfigJsonBody")


@_attrs_define
class SetWorkspaceSlackOauthConfigJsonBody:
    """
    Attributes:
        slack_oauth_client_id (str):
        slack_oauth_client_secret (str):
    """

    slack_oauth_client_id: str
    slack_oauth_client_secret: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        slack_oauth_client_id = self.slack_oauth_client_id
        slack_oauth_client_secret = self.slack_oauth_client_secret

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "slack_oauth_client_id": slack_oauth_client_id,
                "slack_oauth_client_secret": slack_oauth_client_secret,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        slack_oauth_client_id = d.pop("slack_oauth_client_id")

        slack_oauth_client_secret = d.pop("slack_oauth_client_secret")

        set_workspace_slack_oauth_config_json_body = cls(
            slack_oauth_client_id=slack_oauth_client_id,
            slack_oauth_client_secret=slack_oauth_client_secret,
        )

        set_workspace_slack_oauth_config_json_body.additional_properties = d
        return set_workspace_slack_oauth_config_json_body

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
