from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_settings_response_200_ducklake_ducklakes_additional_property_fork_behavior import (
    GetSettingsResponse200DucklakeDucklakesAdditionalPropertyForkBehavior,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_settings_response_200_ducklake_ducklakes_additional_property_catalog import (
        GetSettingsResponse200DucklakeDucklakesAdditionalPropertyCatalog,
    )
    from ..models.get_settings_response_200_ducklake_ducklakes_additional_property_maintenance import (
        GetSettingsResponse200DucklakeDucklakesAdditionalPropertyMaintenance,
    )
    from ..models.get_settings_response_200_ducklake_ducklakes_additional_property_storage import (
        GetSettingsResponse200DucklakeDucklakesAdditionalPropertyStorage,
    )


T = TypeVar("T", bound="GetSettingsResponse200DucklakeDucklakesAdditionalProperty")


@_attrs_define
class GetSettingsResponse200DucklakeDucklakesAdditionalProperty:
    """
    Attributes:
        catalog (GetSettingsResponse200DucklakeDucklakesAdditionalPropertyCatalog):
        storage (GetSettingsResponse200DucklakeDucklakesAdditionalPropertyStorage):
        extra_args (Union[Unset, str]):
        fork_behavior (Union[Unset, GetSettingsResponse200DucklakeDucklakesAdditionalPropertyForkBehavior]): Fork
            workspaces only - how this lake behaves in the fork, stamped at fork creation. Absent = isolated (fork-scoped
            namespace + read-defer to parent).
        maintenance (Union[Unset, GetSettingsResponse200DucklakeDucklakesAdditionalPropertyMaintenance]): Scheduled
            maintenance (enterprise) - snapshot expiry, adjacent-file compaction and orphaned-file cleanup, run as a managed
            per-lake schedule
    """

    catalog: "GetSettingsResponse200DucklakeDucklakesAdditionalPropertyCatalog"
    storage: "GetSettingsResponse200DucklakeDucklakesAdditionalPropertyStorage"
    extra_args: Union[Unset, str] = UNSET
    fork_behavior: Union[Unset, GetSettingsResponse200DucklakeDucklakesAdditionalPropertyForkBehavior] = UNSET
    maintenance: Union[Unset, "GetSettingsResponse200DucklakeDucklakesAdditionalPropertyMaintenance"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        catalog = self.catalog.to_dict()

        storage = self.storage.to_dict()

        extra_args = self.extra_args
        fork_behavior: Union[Unset, str] = UNSET
        if not isinstance(self.fork_behavior, Unset):
            fork_behavior = self.fork_behavior.value

        maintenance: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.maintenance, Unset):
            maintenance = self.maintenance.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "catalog": catalog,
                "storage": storage,
            }
        )
        if extra_args is not UNSET:
            field_dict["extra_args"] = extra_args
        if fork_behavior is not UNSET:
            field_dict["fork_behavior"] = fork_behavior
        if maintenance is not UNSET:
            field_dict["maintenance"] = maintenance

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_settings_response_200_ducklake_ducklakes_additional_property_catalog import (
            GetSettingsResponse200DucklakeDucklakesAdditionalPropertyCatalog,
        )
        from ..models.get_settings_response_200_ducklake_ducklakes_additional_property_maintenance import (
            GetSettingsResponse200DucklakeDucklakesAdditionalPropertyMaintenance,
        )
        from ..models.get_settings_response_200_ducklake_ducklakes_additional_property_storage import (
            GetSettingsResponse200DucklakeDucklakesAdditionalPropertyStorage,
        )

        d = src_dict.copy()
        catalog = GetSettingsResponse200DucklakeDucklakesAdditionalPropertyCatalog.from_dict(d.pop("catalog"))

        storage = GetSettingsResponse200DucklakeDucklakesAdditionalPropertyStorage.from_dict(d.pop("storage"))

        extra_args = d.pop("extra_args", UNSET)

        _fork_behavior = d.pop("fork_behavior", UNSET)
        fork_behavior: Union[Unset, GetSettingsResponse200DucklakeDucklakesAdditionalPropertyForkBehavior]
        if isinstance(_fork_behavior, Unset):
            fork_behavior = UNSET
        else:
            fork_behavior = GetSettingsResponse200DucklakeDucklakesAdditionalPropertyForkBehavior(_fork_behavior)

        _maintenance = d.pop("maintenance", UNSET)
        maintenance: Union[Unset, GetSettingsResponse200DucklakeDucklakesAdditionalPropertyMaintenance]
        if isinstance(_maintenance, Unset):
            maintenance = UNSET
        else:
            maintenance = GetSettingsResponse200DucklakeDucklakesAdditionalPropertyMaintenance.from_dict(_maintenance)

        get_settings_response_200_ducklake_ducklakes_additional_property = cls(
            catalog=catalog,
            storage=storage,
            extra_args=extra_args,
            fork_behavior=fork_behavior,
            maintenance=maintenance,
        )

        get_settings_response_200_ducklake_ducklakes_additional_property.additional_properties = d
        return get_settings_response_200_ducklake_ducklakes_additional_property

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
