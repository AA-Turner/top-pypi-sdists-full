from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingComplianceChecklist")


@_attrs_define
class OfferingComplianceChecklist:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        questions_count (Union[Unset, int]):
    """

    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    questions_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        description = self.description

        questions_count = self.questions_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if questions_count is not UNSET:
            field_dict["questions_count"] = questions_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        questions_count = d.pop("questions_count", UNSET)

        offering_compliance_checklist = cls(
            uuid=uuid,
            name=name,
            description=description,
            questions_count=questions_count,
        )

        offering_compliance_checklist.additional_properties = d
        return offering_compliance_checklist

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
