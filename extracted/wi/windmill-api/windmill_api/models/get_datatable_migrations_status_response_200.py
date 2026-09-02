from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_datatable_migrations_status_response_200_migrations_item import (
        GetDatatableMigrationsStatusResponse200MigrationsItem,
    )


T = TypeVar("T", bound="GetDatatableMigrationsStatusResponse200")


@_attrs_define
class GetDatatableMigrationsStatusResponse200:
    """
    Attributes:
        enabled (bool):
        migrations (List['GetDatatableMigrationsStatusResponse200MigrationsItem']):
        error (Union[Unset, str]):
    """

    enabled: bool
    migrations: List["GetDatatableMigrationsStatusResponse200MigrationsItem"]
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        migrations = []
        for migrations_item_data in self.migrations:
            migrations_item = migrations_item_data.to_dict()

            migrations.append(migrations_item)

        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "migrations": migrations,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_datatable_migrations_status_response_200_migrations_item import (
            GetDatatableMigrationsStatusResponse200MigrationsItem,
        )

        d = src_dict.copy()
        enabled = d.pop("enabled")

        migrations = []
        _migrations = d.pop("migrations")
        for migrations_item_data in _migrations:
            migrations_item = GetDatatableMigrationsStatusResponse200MigrationsItem.from_dict(migrations_item_data)

            migrations.append(migrations_item)

        error = d.pop("error", UNSET)

        get_datatable_migrations_status_response_200 = cls(
            enabled=enabled,
            migrations=migrations,
            error=error,
        )

        get_datatable_migrations_status_response_200.additional_properties = d
        return get_datatable_migrations_status_response_200

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
