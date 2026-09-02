from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_public_settings_response_200_datatable_datatables_additional_property_forked_from_schema import (
        GetPublicSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFromSchema,
    )


T = TypeVar("T", bound="GetPublicSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFrom")


@_attrs_define
class GetPublicSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFrom:
    """Fork origin info with schema snapshot

    Attributes:
        schema (Union[Unset, GetPublicSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFromSchema]): Schema
            snapshot at fork time
    """

    schema: Union[Unset, "GetPublicSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFromSchema"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_public_settings_response_200_datatable_datatables_additional_property_forked_from_schema import (
            GetPublicSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFromSchema,
        )

        d = src_dict.copy()
        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, GetPublicSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFromSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = GetPublicSettingsResponse200DatatableDatatablesAdditionalPropertyForkedFromSchema.from_dict(
                _schema
            )

        get_public_settings_response_200_datatable_datatables_additional_property_forked_from = cls(
            schema=schema,
        )

        get_public_settings_response_200_datatable_datatables_additional_property_forked_from.additional_properties = d
        return get_public_settings_response_200_datatable_datatables_additional_property_forked_from

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
