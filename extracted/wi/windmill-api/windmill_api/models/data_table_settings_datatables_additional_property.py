from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_table_settings_datatables_additional_property_database import (
        DataTableSettingsDatatablesAdditionalPropertyDatabase,
    )
    from ..models.data_table_settings_datatables_additional_property_forked_from import (
        DataTableSettingsDatatablesAdditionalPropertyForkedFrom,
    )
    from ..models.data_table_settings_datatables_additional_property_governed_by import (
        DataTableSettingsDatatablesAdditionalPropertyGovernedBy,
    )
    from ..models.data_table_settings_datatables_additional_property_reference import (
        DataTableSettingsDatatablesAdditionalPropertyReference,
    )


T = TypeVar("T", bound="DataTableSettingsDatatablesAdditionalProperty")


@_attrs_define
class DataTableSettingsDatatablesAdditionalProperty:
    """
    Attributes:
        database (Union[Unset, DataTableSettingsDatatablesAdditionalPropertyDatabase]): Set on an entry that owns its
            database. Absent on a fork's entry, which points at another workspace's data table instead.
        reference (Union[Unset, DataTableSettingsDatatablesAdditionalPropertyReference]): The workspace and data table
            that govern this one. Server-owned: written by fork creation, and carried across a settings save whatever the
            request says.
        governed_by (Union[Unset, DataTableSettingsDatatablesAdditionalPropertyGovernedBy]): On a clone, the data table
            it was copied from, whose roles it takes. Server-owned like `reference`.
        migrations_enabled (Union[Unset, bool]): Whether the SQL migrations feature is opted in for this data table
        forked_from (Union[Unset, DataTableSettingsDatatablesAdditionalPropertyForkedFrom]): Fork origin info with
            schema snapshot
    """

    database: Union[Unset, "DataTableSettingsDatatablesAdditionalPropertyDatabase"] = UNSET
    reference: Union[Unset, "DataTableSettingsDatatablesAdditionalPropertyReference"] = UNSET
    governed_by: Union[Unset, "DataTableSettingsDatatablesAdditionalPropertyGovernedBy"] = UNSET
    migrations_enabled: Union[Unset, bool] = UNSET
    forked_from: Union[Unset, "DataTableSettingsDatatablesAdditionalPropertyForkedFrom"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        database: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.database, Unset):
            database = self.database.to_dict()

        reference: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.reference, Unset):
            reference = self.reference.to_dict()

        governed_by: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.governed_by, Unset):
            governed_by = self.governed_by.to_dict()

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
        if governed_by is not UNSET:
            field_dict["governed_by"] = governed_by
        if migrations_enabled is not UNSET:
            field_dict["migrations_enabled"] = migrations_enabled
        if forked_from is not UNSET:
            field_dict["forked_from"] = forked_from

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data_table_settings_datatables_additional_property_database import (
            DataTableSettingsDatatablesAdditionalPropertyDatabase,
        )
        from ..models.data_table_settings_datatables_additional_property_forked_from import (
            DataTableSettingsDatatablesAdditionalPropertyForkedFrom,
        )
        from ..models.data_table_settings_datatables_additional_property_governed_by import (
            DataTableSettingsDatatablesAdditionalPropertyGovernedBy,
        )
        from ..models.data_table_settings_datatables_additional_property_reference import (
            DataTableSettingsDatatablesAdditionalPropertyReference,
        )

        d = src_dict.copy()
        _database = d.pop("database", UNSET)
        database: Union[Unset, DataTableSettingsDatatablesAdditionalPropertyDatabase]
        if isinstance(_database, Unset):
            database = UNSET
        else:
            database = DataTableSettingsDatatablesAdditionalPropertyDatabase.from_dict(_database)

        _reference = d.pop("reference", UNSET)
        reference: Union[Unset, DataTableSettingsDatatablesAdditionalPropertyReference]
        if isinstance(_reference, Unset):
            reference = UNSET
        else:
            reference = DataTableSettingsDatatablesAdditionalPropertyReference.from_dict(_reference)

        _governed_by = d.pop("governed_by", UNSET)
        governed_by: Union[Unset, DataTableSettingsDatatablesAdditionalPropertyGovernedBy]
        if isinstance(_governed_by, Unset):
            governed_by = UNSET
        else:
            governed_by = DataTableSettingsDatatablesAdditionalPropertyGovernedBy.from_dict(_governed_by)

        migrations_enabled = d.pop("migrations_enabled", UNSET)

        _forked_from = d.pop("forked_from", UNSET)
        forked_from: Union[Unset, DataTableSettingsDatatablesAdditionalPropertyForkedFrom]
        if isinstance(_forked_from, Unset):
            forked_from = UNSET
        else:
            forked_from = DataTableSettingsDatatablesAdditionalPropertyForkedFrom.from_dict(_forked_from)

        data_table_settings_datatables_additional_property = cls(
            database=database,
            reference=reference,
            governed_by=governed_by,
            migrations_enabled=migrations_enabled,
            forked_from=forked_from,
        )

        data_table_settings_datatables_additional_property.additional_properties = d
        return data_table_settings_datatables_additional_property

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
