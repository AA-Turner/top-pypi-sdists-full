import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListResourceTypeResponse200Item")


@_attrs_define
class ListResourceTypeResponse200Item:
    """
    Attributes:
        name (str):
        workspace_id (Union[Unset, str]):
        schema (Union[Unset, Any]):
        description (Union[Unset, str]):
        created_by (Union[Unset, str]):
        edited_at (Union[Unset, datetime.datetime]):
        format_extension (Union[Unset, str]):
    """

    name: str
    workspace_id: Union[Unset, str] = UNSET
    schema: Union[Unset, Any] = UNSET
    description: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    edited_at: Union[Unset, datetime.datetime] = UNSET
    format_extension: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        workspace_id = self.workspace_id
        schema = self.schema
        description = self.description
        created_by = self.created_by
        edited_at: Union[Unset, str] = UNSET
        if not isinstance(self.edited_at, Unset):
            edited_at = self.edited_at.isoformat()

        format_extension = self.format_extension

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if schema is not UNSET:
            field_dict["schema"] = schema
        if description is not UNSET:
            field_dict["description"] = description
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if edited_at is not UNSET:
            field_dict["edited_at"] = edited_at
        if format_extension is not UNSET:
            field_dict["format_extension"] = format_extension

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        workspace_id = d.pop("workspace_id", UNSET)

        schema = d.pop("schema", UNSET)

        description = d.pop("description", UNSET)

        created_by = d.pop("created_by", UNSET)

        _edited_at = d.pop("edited_at", UNSET)
        edited_at: Union[Unset, datetime.datetime]
        if isinstance(_edited_at, Unset):
            edited_at = UNSET
        else:
            edited_at = isoparse(_edited_at)

        format_extension = d.pop("format_extension", UNSET)

        list_resource_type_response_200_item = cls(
            name=name,
            workspace_id=workspace_id,
            schema=schema,
            description=description,
            created_by=created_by,
            edited_at=edited_at,
            format_extension=format_extension,
        )

        list_resource_type_response_200_item.additional_properties = d
        return list_resource_type_response_200_item

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
