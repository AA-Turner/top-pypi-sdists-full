from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.issue_list_dto_item_entity_type_type_0 import IssueListDtoItemEntityTypeType0
from ..models.issue_list_dto_item_status import IssueListDtoItemStatus
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="IssueListDtoItem")



@_attrs_define
class IssueListDtoItem:
    """ An author-flagged note attached to a problem or one of its child entities.

        Attributes:
            id (UUID): Stable issue identifier (UUID). Issues are author-flagged notes attached to a problem.
            problem_id (UUID): Stable problem identifier (UUID).
            entity_type (IssueListDtoItemEntityTypeType0 | None): Optional child entity type the issue is anchored to. Null
                when the issue is attached to the problem itself.
            entity_id (None | UUID): Identifier of the child entity the issue is anchored to. Null when no child entity is
                attached.
            created_by_id (None | UUID): User who created the issue. Null for system-authored issues.
            description (str): Markdown body of the issue.
            status (IssueListDtoItemStatus): Current lifecycle status of the issue.
            created_at (datetime.datetime): Timestamp when the issue was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the issue was last updated (ISO-8601, UTC).
     """

    id: UUID
    problem_id: UUID
    entity_type: IssueListDtoItemEntityTypeType0 | None
    entity_id: None | UUID
    created_by_id: None | UUID
    description: str
    status: IssueListDtoItemStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        problem_id = str(self.problem_id)

        entity_type: None | str
        if isinstance(self.entity_type, IssueListDtoItemEntityTypeType0):
            entity_type = self.entity_type.value
        else:
            entity_type = self.entity_type

        entity_id: None | str
        if isinstance(self.entity_id, UUID):
            entity_id = str(self.entity_id)
        else:
            entity_id = self.entity_id

        created_by_id: None | str
        if isinstance(self.created_by_id, UUID):
            created_by_id = str(self.created_by_id)
        else:
            created_by_id = self.created_by_id

        description = self.description

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "problemId": problem_id,
            "entityType": entity_type,
            "entityId": entity_id,
            "createdById": created_by_id,
            "description": description,
            "status": status,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        problem_id = UUID(d.pop("problemId"))




        def _parse_entity_type(data: object) -> IssueListDtoItemEntityTypeType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                entity_type_type_0 = IssueListDtoItemEntityTypeType0(data)



                return entity_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(IssueListDtoItemEntityTypeType0 | None, data)

        entity_type = _parse_entity_type(d.pop("entityType"))


        def _parse_entity_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                entity_id_type_0 = UUID(data)



                return entity_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        entity_id = _parse_entity_id(d.pop("entityId"))


        def _parse_created_by_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_by_id_type_0 = UUID(data)



                return created_by_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        created_by_id = _parse_created_by_id(d.pop("createdById"))


        description = d.pop("description")

        status = IssueListDtoItemStatus(d.pop("status"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        issue_list_dto_item = cls(
            id=id,
            problem_id=problem_id,
            entity_type=entity_type,
            entity_id=entity_id,
            created_by_id=created_by_id,
            description=description,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )

        return issue_list_dto_item

