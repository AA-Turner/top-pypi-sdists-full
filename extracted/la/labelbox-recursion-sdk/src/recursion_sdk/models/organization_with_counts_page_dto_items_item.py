from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="OrganizationWithCountsPageDtoItemsItem")



@_attrs_define
class OrganizationWithCountsPageDtoItemsItem:
    """ An organization enriched with rolled-up counts of its owned resources.

        Attributes:
            id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
            external_id (str): External organization identifier provided by the caller's source-of-truth system.
            name (str): Human-readable display name of the organization.
            created_at (datetime.datetime): Timestamp when the organization was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the organization was last updated (ISO-8601, UTC).
            environment_count (int): Number of environments owned by this organization.
            problem_count (int): Number of problems across all environments owned by this organization.
            problem_run_count (int): Number of problem runs executed across all problems owned by this organization.
     """

    id: UUID
    external_id: str
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    environment_count: int
    problem_count: int
    problem_run_count: int





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        external_id = self.external_id

        name = self.name

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        environment_count = self.environment_count

        problem_count = self.problem_count

        problem_run_count = self.problem_run_count


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "externalId": external_id,
            "name": name,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "environmentCount": environment_count,
            "problemCount": problem_count,
            "problemRunCount": problem_run_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        external_id = d.pop("externalId")

        name = d.pop("name")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        environment_count = d.pop("environmentCount")

        problem_count = d.pop("problemCount")

        problem_run_count = d.pop("problemRunCount")

        organization_with_counts_page_dto_items_item = cls(
            id=id,
            external_id=external_id,
            name=name,
            created_at=created_at,
            updated_at=updated_at,
            environment_count=environment_count,
            problem_count=problem_count,
            problem_run_count=problem_run_count,
        )

        return organization_with_counts_page_dto_items_item

