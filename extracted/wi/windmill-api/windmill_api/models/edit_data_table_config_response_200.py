from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_data_table_config_response_200_stranded_references_item import (
        EditDataTableConfigResponse200StrandedReferencesItem,
    )


T = TypeVar("T", bound="EditDataTableConfigResponse200")


@_attrs_define
class EditDataTableConfigResponse200:
    """
    Attributes:
        stranded_references (Union[Unset, List['EditDataTableConfigResponse200StrandedReferencesItem']]): Data tables in
            other workspaces that were governed by one this save deleted and no longer resolve.
    """

    stranded_references: Union[Unset, List["EditDataTableConfigResponse200StrandedReferencesItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        stranded_references: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.stranded_references, Unset):
            stranded_references = []
            for stranded_references_item_data in self.stranded_references:
                stranded_references_item = stranded_references_item_data.to_dict()

                stranded_references.append(stranded_references_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if stranded_references is not UNSET:
            field_dict["stranded_references"] = stranded_references

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_data_table_config_response_200_stranded_references_item import (
            EditDataTableConfigResponse200StrandedReferencesItem,
        )

        d = src_dict.copy()
        stranded_references = []
        _stranded_references = d.pop("stranded_references", UNSET)
        for stranded_references_item_data in _stranded_references or []:
            stranded_references_item = EditDataTableConfigResponse200StrandedReferencesItem.from_dict(
                stranded_references_item_data
            )

            stranded_references.append(stranded_references_item)

        edit_data_table_config_response_200 = cls(
            stranded_references=stranded_references,
        )

        edit_data_table_config_response_200.additional_properties = d
        return edit_data_table_config_response_200

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
