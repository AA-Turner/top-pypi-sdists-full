from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SecretMigrationFailure")


@_attrs_define
class SecretMigrationFailure:
    """
    Attributes:
        workspace_id (str): Workspace ID where the secret is located
        path (str): Path of the secret that failed to migrate
        error (str): Error message
    """

    workspace_id: str
    path: str
    error: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        path = self.path
        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_id": workspace_id,
                "path": path,
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        path = d.pop("path")

        error = d.pop("error")

        secret_migration_failure = cls(
            workspace_id=workspace_id,
            path=path,
            error=error,
        )

        secret_migration_failure.additional_properties = d
        return secret_migration_failure

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
