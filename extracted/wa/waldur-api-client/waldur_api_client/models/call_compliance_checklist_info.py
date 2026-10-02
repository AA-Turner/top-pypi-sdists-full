from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CallComplianceChecklistInfo")


@_attrs_define
class CallComplianceChecklistInfo:
    """
    Attributes:
        uuid (UUID):
        name (str):
        description (str):
        total_questions (int):
        required_questions (int):
    """

    uuid: UUID
    name: str
    description: str
    total_questions: int
    required_questions: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        description = self.description

        total_questions = self.total_questions

        required_questions = self.required_questions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "description": description,
                "total_questions": total_questions,
                "required_questions": required_questions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        description = d.pop("description")

        total_questions = d.pop("total_questions")

        required_questions = d.pop("required_questions")

        call_compliance_checklist_info = cls(
            uuid=uuid,
            name=name,
            description=description,
            total_questions=total_questions,
            required_questions=required_questions,
        )

        call_compliance_checklist_info.additional_properties = d
        return call_compliance_checklist_info

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
