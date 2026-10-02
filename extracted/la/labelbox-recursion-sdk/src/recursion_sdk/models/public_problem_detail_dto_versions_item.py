from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="PublicProblemDetailDtoVersionsItem")



@_attrs_define
class PublicProblemDetailDtoVersionsItem:
    """ Public read-only projection of a locked problem version — no grading config or bindings.

        Attributes:
            id (UUID): Stable problem-version identifier (UUID). Each problem can have many versions; this points at one
                specific version.
            version (str): Sequential version label assigned at creation (e.g. "v1", "v2"). Example: v3.
            prompt (str): Task prompt shown to the agent at run start.
            locked_at (datetime.datetime): Timestamp when the version was locked (ISO-8601, UTC). Always set — only locked
                versions are exposed publicly.
     """

    id: UUID
    version: str
    prompt: str
    locked_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        version = self.version

        prompt = self.prompt

        locked_at = self.locked_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "version": version,
            "prompt": prompt,
            "lockedAt": locked_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        version = d.pop("version")

        prompt = d.pop("prompt")

        locked_at = datetime.datetime.fromisoformat(d.pop("lockedAt"))




        public_problem_detail_dto_versions_item = cls(
            id=id,
            version=version,
            prompt=prompt,
            locked_at=locked_at,
        )

        return public_problem_detail_dto_versions_item

