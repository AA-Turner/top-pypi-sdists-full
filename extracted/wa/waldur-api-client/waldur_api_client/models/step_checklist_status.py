from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="StepChecklistStatus")


@_attrs_define
class StepChecklistStatus:
    """
    Attributes:
        has_checklist (bool):
        checklist_required (bool):
        checklist_name (Union[None, str]):
        checklist_completed (bool):
        unanswered_required_count (int):
    """

    has_checklist: bool
    checklist_required: bool
    checklist_name: Union[None, str]
    checklist_completed: bool
    unanswered_required_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_checklist = self.has_checklist

        checklist_required = self.checklist_required

        checklist_name: Union[None, str]
        checklist_name = self.checklist_name

        checklist_completed = self.checklist_completed

        unanswered_required_count = self.unanswered_required_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_checklist": has_checklist,
                "checklist_required": checklist_required,
                "checklist_name": checklist_name,
                "checklist_completed": checklist_completed,
                "unanswered_required_count": unanswered_required_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        has_checklist = d.pop("has_checklist")

        checklist_required = d.pop("checklist_required")

        def _parse_checklist_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        checklist_name = _parse_checklist_name(d.pop("checklist_name"))

        checklist_completed = d.pop("checklist_completed")

        unanswered_required_count = d.pop("unanswered_required_count")

        step_checklist_status = cls(
            has_checklist=has_checklist,
            checklist_required=checklist_required,
            checklist_name=checklist_name,
            checklist_completed=checklist_completed,
            unanswered_required_count=unanswered_required_count,
        )

        step_checklist_status.additional_properties = d
        return step_checklist_status

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
