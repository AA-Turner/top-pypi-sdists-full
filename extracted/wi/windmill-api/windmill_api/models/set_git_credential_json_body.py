from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SetGitCredentialJsonBody")


@_attrs_define
class SetGitCredentialJsonBody:
    """
    Attributes:
        repo_url (str): The repository the credential is for, and the key it is stored under. It is served for this
            repository and no other, so repointing a resource elsewhere cannot carry the token along.
        token (str): The access token, as pasted
    """

    repo_url: str
    token: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        repo_url = self.repo_url
        token = self.token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "repo_url": repo_url,
                "token": token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        repo_url = d.pop("repo_url")

        token = d.pop("token")

        set_git_credential_json_body = cls(
            repo_url=repo_url,
            token=token,
        )

        set_git_credential_json_body.additional_properties = d
        return set_git_credential_json_body

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
