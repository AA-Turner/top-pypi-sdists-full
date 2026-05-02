from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_settings_response_200_datatable_datatables_additional_property_database import (
        GetSettingsResponse200DatatableDatatablesAdditionalPropertyDatabase,
    )
    from ..models.get_settings_response_200_datatable_datatables_additional_property_forked_from import (
        GetSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFrom,
    )


T = TypeVar("T", bound="GetSettingsResponse200DatatableDatatablesAdditionalProperty")


@_attrs_define
class GetSettingsResponse200DatatableDatatablesAdditionalProperty:
    """
    Attributes:
        database (GetSettingsResponse200DatatableDatatablesAdditionalPropertyDatabase):
        forked_from (Union[Unset, GetSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFrom]): Fork origin
            info with schema snapshot
    """

    database: "GetSettingsResponse200DatatableDatatablesAdditionalPropertyDatabase"
    forked_from: Union[Unset, "GetSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFrom"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        database = self.database.to_dict()

        forked_from: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.forked_from, Unset):
            forked_from = self.forked_from.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "database": database,
            }
        )
        if forked_from is not UNSET:
            field_dict["forked_from"] = forked_from

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_settings_response_200_datatable_datatables_additional_property_database import (
            GetSettingsResponse200DatatableDatatablesAdditionalPropertyDatabase,
        )
        from ..models.get_settings_response_200_datatable_datatables_additional_property_forked_from import (
            GetSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFrom,
        )

        d = src_dict.copy()
        database = GetSettingsResponse200DatatableDatatablesAdditionalPropertyDatabase.from_dict(d.pop("database"))

        _forked_from = d.pop("forked_from", UNSET)
        forked_from: Union[Unset, GetSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFrom]
        if isinstance(_forked_from, Unset):
            forked_from = UNSET
        else:
            forked_from = GetSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFrom.from_dict(_forked_from)

        get_settings_response_200_datatable_datatables_additional_property = cls(
            database=database,
            forked_from=forked_from,
        )

        get_settings_response_200_datatable_datatables_additional_property.additional_properties = d
        return get_settings_response_200_datatable_datatables_additional_property

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
