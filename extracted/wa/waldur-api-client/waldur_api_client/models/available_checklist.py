from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AvailableChecklist")


@_attrs_define
class AvailableChecklist:
    """
    Attributes:
        uuid (UUID):
        name (str):
        description (str):
        checklist_type (str):
        questions_count (int):
        category_name (Union[None, str]):
        category_uuid (Union[None, UUID]):
    """

    uuid: UUID
    name: str
    description: str
    checklist_type: str
    questions_count: int
    category_name: Union[None, str]
    category_uuid: Union[None, UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        description = self.description

        checklist_type = self.checklist_type

        questions_count = self.questions_count

        category_name: Union[None, str]
        category_name = self.category_name

        category_uuid: Union[None, str]
        if isinstance(self.category_uuid, UUID):
            category_uuid = str(self.category_uuid)
        else:
            category_uuid = self.category_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "description": description,
                "checklist_type": checklist_type,
                "questions_count": questions_count,
                "category_name": category_name,
                "category_uuid": category_uuid,
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

        questions_count = d.pop("questions_count")

        def _parse_category_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        category_name = _parse_category_name(d.pop("category_name"))

        def _parse_category_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                category_uuid_type_0 = UUID(data)

                return category_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        category_uuid = _parse_category_uuid(d.pop("category_uuid"))

        available_checklist = cls(
            uuid=uuid,
            name=name,
            description=description,
            checklist_type=checklist_type,
            questions_count=questions_count,
            category_name=category_name,
            category_uuid=category_uuid,
        )

        available_checklist.additional_properties = d
        return available_checklist

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
