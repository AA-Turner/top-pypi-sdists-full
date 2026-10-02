from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.checklist_type_enum import ChecklistTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="Checklist")


@_attrs_define
class Checklist:
    """
    Attributes:
        uuid (UUID):
        url (str):
        name (str):
        questions_count (int):
        description (Union[Unset, str]):
        checklist_type (Union[Unset, ChecklistTypeEnum]):
    """

    uuid: UUID
    url: str
    name: str
    questions_count: int
    description: Union[Unset, str] = UNSET
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        name = self.name

        questions_count = self.questions_count

        description = self.description

        checklist_type: Union[Unset, str] = UNSET
        if not isinstance(self.checklist_type, Unset):
            checklist_type = self.checklist_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "name": name,
                "questions_count": questions_count,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if checklist_type is not UNSET:
            field_dict["checklist_type"] = checklist_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        name = d.pop("name")

        questions_count = d.pop("questions_count")

        description = d.pop("description", UNSET)

        _checklist_type = d.pop("checklist_type", UNSET)
        checklist_type: Union[Unset, ChecklistTypeEnum]
        if isinstance(_checklist_type, Unset):
            checklist_type = UNSET
        else:
            checklist_type = ChecklistTypeEnum(_checklist_type)

        checklist = cls(
            uuid=uuid,
            url=url,
            name=name,
            questions_count=questions_count,
            description=description,
            checklist_type=checklist_type,
        )

        checklist.additional_properties = d
        return checklist

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
