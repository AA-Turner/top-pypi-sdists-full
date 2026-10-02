from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ChecklistShort")


@_attrs_define
class ChecklistShort:
    """
    Attributes:
        uuid (UUID):
        name (str):
        description (str):
        checklist_type (str):
    """

    uuid: UUID
    name: str
    description: str
    checklist_type: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        description = self.description

        checklist_type = self.checklist_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "description": description,
                "checklist_type": checklist_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        description = d.pop("description")

        checklist_type = d.pop("checklist_type")

        checklist_short = cls(
            uuid=uuid,
            name=name,
            description=description,
            checklist_type=checklist_type,
        )

        checklist_short.additional_properties = d
        return checklist_short

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
