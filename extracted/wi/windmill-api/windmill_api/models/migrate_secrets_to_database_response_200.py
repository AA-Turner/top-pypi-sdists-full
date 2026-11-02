from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.migrate_secrets_to_database_response_200_failures_item import (
        MigrateSecretsToDatabaseResponse200FailuresItem,
    )


T = TypeVar("T", bound="MigrateSecretsToDatabaseResponse200")


@_attrs_define
class MigrateSecretsToDatabaseResponse200:
    """
    Attributes:
        total_secrets (int): Total number of secrets found
        migrated_count (int): Number of secrets successfully migrated
        failed_count (int): Number of secrets that failed to migrate
        failures (List['MigrateSecretsToDatabaseResponse200FailuresItem']): Details of any failures encountered during
            migration
    """

    total_secrets: int
    migrated_count: int
    failed_count: int
    failures: List["MigrateSecretsToDatabaseResponse200FailuresItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_secrets = self.total_secrets
        migrated_count = self.migrated_count
        failed_count = self.failed_count
        failures = []
        for failures_item_data in self.failures:
            failures_item = failures_item_data.to_dict()

            failures.append(failures_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_secrets": total_secrets,
                "migrated_count": migrated_count,
                "failed_count": failed_count,
                "failures": failures,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.migrate_secrets_to_database_response_200_failures_item import (
            MigrateSecretsToDatabaseResponse200FailuresItem,
        )

        d = src_dict.copy()
        total_secrets = d.pop("total_secrets")

        migrated_count = d.pop("migrated_count")

        failed_count = d.pop("failed_count")

        failures = []
        _failures = d.pop("failures")
        for failures_item_data in _failures:
            failures_item = MigrateSecretsToDatabaseResponse200FailuresItem.from_dict(failures_item_data)

            failures.append(failures_item)

        migrate_secrets_to_database_response_200 = cls(
            total_secrets=total_secrets,
            migrated_count=migrated_count,
            failed_count=failed_count,
            failures=failures,
        )

        migrate_secrets_to_database_response_200.additional_properties = d
        return migrate_secrets_to_database_response_200

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
