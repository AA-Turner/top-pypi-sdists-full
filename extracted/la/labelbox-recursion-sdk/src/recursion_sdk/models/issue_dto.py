from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.issue_dto_entity_type_type_0 import IssueDtoEntityTypeType0
from ..models.issue_dto_status import IssueDtoStatus
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="IssueDto")



@_attrs_define
class IssueDto:
    """ An author-flagged note attached to a problem or one of its child entities.

        Example:
            {'id': 'e12cb018-b24c-4b35-9d8d-e7b486eb4e95', 'problemId': '2d3fe029-a7d1-4747-9d09-81b976087bbb',
                'entityType': None, 'entityId': None, 'createdById': '49dea803-7390-49c4-abb1-5629718fc9cd', 'description': 'The
                "detect-surface-defects" prompt is ambiguous about hairline scratches: it does not say whether sub-0.5mm
                scratches count as defects, so graders disagree on the expected label. Please clarify the threshold in the task
                description.', 'status': 'open', 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt':
                '2026-01-16T14:20:00.000Z'}

        Attributes:
            id (UUID): Stable issue identifier (UUID). Issues are author-flagged notes attached to a problem.
            problem_id (UUID): Stable problem identifier (UUID).
            entity_type (IssueDtoEntityTypeType0 | None): Optional child entity type the issue is anchored to. Null when the
                issue is attached to the problem itself.
            entity_id (None | UUID): Identifier of the child entity the issue is anchored to. Null when no child entity is
                attached.
            created_by_id (None | UUID): User who created the issue. Null for system-authored issues.
            description (str): Markdown body of the issue.
            status (IssueDtoStatus): Current lifecycle status of the issue.
            created_at (datetime.datetime): Timestamp when the issue was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the issue was last updated (ISO-8601, UTC).
     """

    id: UUID
    problem_id: UUID
    entity_type: IssueDtoEntityTypeType0 | None
    entity_id: None | UUID
    created_by_id: None | UUID
    description: str
    status: IssueDtoStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        problem_id = str(self.problem_id)

        entity_type: None | str
        if isinstance(self.entity_type, IssueDtoEntityTypeType0):
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




        def _parse_entity_type(data: object) -> IssueDtoEntityTypeType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                entity_type_type_0 = IssueDtoEntityTypeType0(data)



                return entity_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(IssueDtoEntityTypeType0 | None, data)

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

        status = IssueDtoStatus(d.pop("status"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        issue_dto = cls(
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

        return issue_dto

