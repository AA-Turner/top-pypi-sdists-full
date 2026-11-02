from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_data_table_config_json_body_renames_item import EditDataTableConfigJsonBodyRenamesItem
    from ..models.edit_data_table_config_json_body_settings import EditDataTableConfigJsonBodySettings


T = TypeVar("T", bound="EditDataTableConfigJsonBody")


@_attrs_define
class EditDataTableConfigJsonBody:
    """
    Attributes:
        settings (EditDataTableConfigJsonBodySettings):
        renames (Union[Unset, List['EditDataTableConfigJsonBodyRenamesItem']]): data tables renamed in this save, so
            their migrations cascade
        deleted_datatables (Union[Unset, List[str]]): data tables removed in this save, so their migrations are deleted
    """

    settings: "EditDataTableConfigJsonBodySettings"
    renames: Union[Unset, List["EditDataTableConfigJsonBodyRenamesItem"]] = UNSET
    deleted_datatables: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        settings = self.settings.to_dict()

        renames: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.renames, Unset):
            renames = []
            for renames_item_data in self.renames:
                renames_item = renames_item_data.to_dict()

                renames.append(renames_item)

        deleted_datatables: Union[Unset, List[str]] = UNSET
        if not isinstance(self.deleted_datatables, Unset):
            deleted_datatables = self.deleted_datatables

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "settings": settings,
            }
        )
        if renames is not UNSET:
            field_dict["renames"] = renames
        if deleted_datatables is not UNSET:
            field_dict["deleted_datatables"] = deleted_datatables

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_data_table_config_json_body_renames_item import EditDataTableConfigJsonBodyRenamesItem
        from ..models.edit_data_table_config_json_body_settings import EditDataTableConfigJsonBodySettings

        d = src_dict.copy()
        settings = EditDataTableConfigJsonBodySettings.from_dict(d.pop("settings"))

        renames = []
        _renames = d.pop("renames", UNSET)
        for renames_item_data in _renames or []:
            renames_item = EditDataTableConfigJsonBodyRenamesItem.from_dict(renames_item_data)

            renames.append(renames_item)

        deleted_datatables = cast(List[str], d.pop("deleted_datatables", UNSET))

        edit_data_table_config_json_body = cls(
            settings=settings,
            renames=renames,
            deleted_datatables=deleted_datatables,
        )

        edit_data_table_config_json_body.additional_properties = d
        return edit_data_table_config_json_body

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
