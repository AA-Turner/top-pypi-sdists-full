from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_data_table_config_json_body_settings_datatables_additional_property_database import (
        EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabase,
    )
    from ..models.edit_data_table_config_json_body_settings_datatables_additional_property_forked_from import (
        EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyForkedFrom,
    )
    from ..models.edit_data_table_config_json_body_settings_datatables_additional_property_reference import (
        EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyReference,
    )


T = TypeVar("T", bound="EditDataTableConfigJsonBodySettingsDatatablesAdditionalProperty")


@_attrs_define
class EditDataTableConfigJsonBodySettingsDatatablesAdditionalProperty:
    """
    Attributes:
        database (Union[Unset, EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabase]): Set on an
            entry that owns its database. Absent on a fork's entry, which points at another workspace's data table instead.
        reference (Union[Unset, EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyReference]): The
            workspace and data table that govern this one. Server-owned: written by fork creation, and carried across a
            settings save whatever the request says.
        migrations_enabled (Union[Unset, bool]): Whether the SQL migrations feature is opted in for this data table
        forked_from (Union[Unset, EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyForkedFrom]): Fork
            origin info with schema snapshot
    """

    database: Union[Unset, "EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabase"] = UNSET
    reference: Union[Unset, "EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyReference"] = UNSET
    migrations_enabled: Union[Unset, bool] = UNSET
    forked_from: Union[Unset, "EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyForkedFrom"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        database: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.database, Unset):
            database = self.database.to_dict()

        reference: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.reference, Unset):
            reference = self.reference.to_dict()

        migrations_enabled = self.migrations_enabled
        forked_from: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.forked_from, Unset):
            forked_from = self.forked_from.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if database is not UNSET:
            field_dict["database"] = database
        if reference is not UNSET:
            field_dict["reference"] = reference
        if migrations_enabled is not UNSET:
            field_dict["migrations_enabled"] = migrations_enabled
        if forked_from is not UNSET:
            field_dict["forked_from"] = forked_from

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_data_table_config_json_body_settings_datatables_additional_property_database import (
            EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabase,
        )
        from ..models.edit_data_table_config_json_body_settings_datatables_additional_property_forked_from import (
            EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyForkedFrom,
        )
        from ..models.edit_data_table_config_json_body_settings_datatables_additional_property_reference import (
            EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyReference,
        )

        d = src_dict.copy()
        _database = d.pop("database", UNSET)
        database: Union[Unset, EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabase]
        if isinstance(_database, Unset):
            database = UNSET
        else:
            database = EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabase.from_dict(_database)

        _reference = d.pop("reference", UNSET)
        reference: Union[Unset, EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyReference]
        if isinstance(_reference, Unset):
            reference = UNSET
        else:
            reference = EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyReference.from_dict(_reference)

        migrations_enabled = d.pop("migrations_enabled", UNSET)

        _forked_from = d.pop("forked_from", UNSET)
        forked_from: Union[Unset, EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyForkedFrom]
        if isinstance(_forked_from, Unset):
            forked_from = UNSET
        else:
            forked_from = EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyForkedFrom.from_dict(
                _forked_from
            )

        edit_data_table_config_json_body_settings_datatables_additional_property = cls(
            database=database,
            reference=reference,
            migrations_enabled=migrations_enabled,
            forked_from=forked_from,
        )

        edit_data_table_config_json_body_settings_datatables_additional_property.additional_properties = d
        return edit_data_table_config_json_body_settings_datatables_additional_property

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
