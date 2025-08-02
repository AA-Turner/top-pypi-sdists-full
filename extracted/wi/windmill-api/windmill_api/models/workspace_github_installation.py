from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkspaceGithubInstallation")


@_attrs_define
class WorkspaceGithubInstallation:
    """
    Attributes:
        account_id (str):
        installation_id (float):
    """

    account_id: str
    installation_id: float
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_id = self.account_id
        installation_id = self.installation_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_id": account_id,
                "installation_id": installation_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        account_id = d.pop("account_id")

        installation_id = d.pop("installation_id")

        workspace_github_installation = cls(
            account_id=account_id,
            installation_id=installation_id,
        )

        workspace_github_installation.additional_properties = d
        return workspace_github_installation

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
