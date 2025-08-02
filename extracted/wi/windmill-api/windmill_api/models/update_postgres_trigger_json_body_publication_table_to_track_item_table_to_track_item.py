from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdatePostgresTriggerJsonBodyPublicationTableToTrackItemTableToTrackItem")


@_attrs_define
class UpdatePostgresTriggerJsonBodyPublicationTableToTrackItemTableToTrackItem:
    """
    Attributes:
        table_name (str):
        columns_name (Union[Unset, List[str]]):
        where_clause (Union[Unset, str]):
    """

    table_name: str
    columns_name: Union[Unset, List[str]] = UNSET
    where_clause: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        table_name = self.table_name
        columns_name: Union[Unset, List[str]] = UNSET
        if not isinstance(self.columns_name, Unset):
            columns_name = self.columns_name

        where_clause = self.where_clause

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "table_name": table_name,
            }
        )
        if columns_name is not UNSET:
            field_dict["columns_name"] = columns_name
        if where_clause is not UNSET:
            field_dict["where_clause"] = where_clause

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        table_name = d.pop("table_name")

        columns_name = cast(List[str], d.pop("columns_name", UNSET))

        where_clause = d.pop("where_clause", UNSET)

        update_postgres_trigger_json_body_publication_table_to_track_item_table_to_track_item = cls(
            table_name=table_name,
            columns_name=columns_name,
            where_clause=where_clause,
        )

        update_postgres_trigger_json_body_publication_table_to_track_item_table_to_track_item.additional_properties = d
        return update_postgres_trigger_json_body_publication_table_to_track_item_table_to_track_item

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
