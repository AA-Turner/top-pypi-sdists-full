from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetSettingsResponse200DatatableDatatablesAdditionalPropertyReference")


@_attrs_define
class GetSettingsResponse200DatatableDatatablesAdditionalPropertyReference:
    """The workspace and data table that govern this one. Server-owned: written by fork creation, and carried across a
    settings save whatever the request says.

        Attributes:
            workspace_id (str):
            datatable (str):
    """

    workspace_id: str
    datatable: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        datatable = self.datatable

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_id": workspace_id,
                "datatable": datatable,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        datatable = d.pop("datatable")

        get_settings_response_200_datatable_datatables_additional_property_reference = cls(
            workspace_id=workspace_id,
            datatable=datatable,
        )

        get_settings_response_200_datatable_datatables_additional_property_reference.additional_properties = d
        return get_settings_response_200_datatable_datatables_additional_property_reference

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
