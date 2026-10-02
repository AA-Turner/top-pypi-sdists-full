from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.transcript_dto_source_type import TranscriptDtoSourceType
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="TranscriptDto")



@_attrs_define
class TranscriptDto:
    """ Stored request/response log produced by a single source run (solver, grader, or synthesizer).

        Attributes:
            id (UUID): Stable transcript identifier (UUID). Captures the request / response log of a problem run.
            source_type (TranscriptDtoSourceType): Origin run type that produced the transcript content.
            source_id (UUID): UUID of the source run (problem_run, grading_run, rubric_score, or synthesizer_run).
            content (str): Raw serialized transcript content (typically newline-delimited JSON events).
            created_at (datetime.datetime): Timestamp when the transcript was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the transcript was last updated (ISO-8601, UTC).
     """

    id: UUID
    source_type: TranscriptDtoSourceType
    source_id: UUID
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        source_type = self.source_type.value

        source_id = str(self.source_id)

        content = self.content

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "sourceType": source_type,
            "sourceId": source_id,
            "content": content,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        source_type = TranscriptDtoSourceType(d.pop("sourceType"))




        source_id = UUID(d.pop("sourceId"))




        content = d.pop("content")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        transcript_dto = cls(
            id=id,
            source_type=source_type,
            source_id=source_id,
            content=content,
            created_at=created_at,
            updated_at=updated_at,
        )

        return transcript_dto

