from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_issue_body_dto_entity_type import CreateIssueBodyDtoEntityType
from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="CreateIssueBodyDto")



@_attrs_define
class CreateIssueBodyDto:
    """ Request body for creating an issue on a problem.

        Example:
            {'description': 'The "detect-surface-defects" prompt is ambiguous about hairline scratches: it does not say
                whether sub-0.5mm scratches count as defects, so graders disagree on the expected label. Please clarify the
                threshold in the task description.'}

        Attributes:
            description (str): Markdown body of the new issue.
            entity_type (CreateIssueBodyDtoEntityType | Unset): Optional child entity type to attach the issue to. Must be
                provided together with the entity identifier.
            entity_id (UUID | Unset): Identifier of the child entity to attach the issue to. Must be provided together with
                the entity type.
     """

    description: str
    entity_type: CreateIssueBodyDtoEntityType | Unset = UNSET
    entity_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        entity_type: str | Unset = UNSET
        if not isinstance(self.entity_type, Unset):
            entity_type = self.entity_type.value


        entity_id: str | Unset = UNSET
        if not isinstance(self.entity_id, Unset):
            entity_id = str(self.entity_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "description": description,
        })
        if entity_type is not UNSET:
            field_dict["entityType"] = entity_type
        if entity_id is not UNSET:
            field_dict["entityId"] = entity_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        _entity_type = d.pop("entityType", UNSET)
        entity_type: CreateIssueBodyDtoEntityType | Unset
        if isinstance(_entity_type,  Unset):
            entity_type = UNSET
        else:
            entity_type = CreateIssueBodyDtoEntityType(_entity_type)




        _entity_id = d.pop("entityId", UNSET)
        entity_id: UUID | Unset
        if isinstance(_entity_id,  Unset):
            entity_id = UNSET
        else:
            entity_id = UUID(_entity_id)




        create_issue_body_dto = cls(
            description=description,
            entity_type=entity_type,
            entity_id=entity_id,
        )


        create_issue_body_dto.additional_properties = d
        return create_issue_body_dto

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
