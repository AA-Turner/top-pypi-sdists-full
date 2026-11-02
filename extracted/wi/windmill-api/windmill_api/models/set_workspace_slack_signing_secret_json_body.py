from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetWorkspaceSlackSigningSecretJsonBody")


@_attrs_define
class SetWorkspaceSlackSigningSecretJsonBody:
    """
    Attributes:
        slack_signing_secret (Union[Unset, None, str]):
    """

    slack_signing_secret: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        slack_signing_secret = self.slack_signing_secret

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if slack_signing_secret is not UNSET:
            field_dict["slack_signing_secret"] = slack_signing_secret

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        slack_signing_secret = d.pop("slack_signing_secret", UNSET)

        set_workspace_slack_signing_secret_json_body = cls(
            slack_signing_secret=slack_signing_secret,
        )

        set_workspace_slack_signing_secret_json_body.additional_properties = d
        return set_workspace_slack_signing_secret_json_body

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
