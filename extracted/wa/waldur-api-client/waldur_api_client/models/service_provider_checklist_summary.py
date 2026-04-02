from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ServiceProviderChecklistSummary")


@_attrs_define
class ServiceProviderChecklistSummary:
    """
    Attributes:
        checklist_uuid (UUID):
        checklist_name (str):
        questions_count (int):
        offerings_count (int):
    """

    checklist_uuid: UUID
    checklist_name: str
    questions_count: int
    offerings_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checklist_uuid = str(self.checklist_uuid)

        checklist_name = self.checklist_name

        questions_count = self.questions_count

        offerings_count = self.offerings_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checklist_uuid": checklist_uuid,
                "checklist_name": checklist_name,
                "questions_count": questions_count,
                "offerings_count": offerings_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        checklist_uuid = UUID(d.pop("checklist_uuid"))

        checklist_name = d.pop("checklist_name")

        questions_count = d.pop("questions_count")

        offerings_count = d.pop("offerings_count")

        service_provider_checklist_summary = cls(
            checklist_uuid=checklist_uuid,
            checklist_name=checklist_name,
            questions_count=questions_count,
            offerings_count=offerings_count,
        )

        service_provider_checklist_summary.additional_properties = d
        return service_provider_checklist_summary

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
