from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="TemplateResponseDto")



@_attrs_define
class TemplateResponseDto:
    """ Identifies the template problem and its current version for an environment.

        Example:
            {'problemId': '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'versionId': '0c3ac467-57e1-4074-b57d-b6a7be392f71'}

        Attributes:
            problem_id (UUID): Stable problem identifier (UUID).
            version_id (UUID): Stable problem-version identifier (UUID). Each problem can have many versions; this points at
                one specific version.
            created (bool | Unset): True when the template was created by this request, false when an existing template was
                returned. Omitted on endpoints that do not distinguish.
     """

    problem_id: UUID
    version_id: UUID
    created: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        problem_id = str(self.problem_id)

        version_id = str(self.version_id)

        created = self.created


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "problemId": problem_id,
            "versionId": version_id,
        })
        if created is not UNSET:
            field_dict["created"] = created

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        problem_id = UUID(d.pop("problemId"))




        version_id = UUID(d.pop("versionId"))




        created = d.pop("created", UNSET)

        template_response_dto = cls(
            problem_id=problem_id,
            version_id=version_id,
            created=created,
        )

        return template_response_dto

