from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="CreateProblemsResponseDtoProblemsItem")



@_attrs_define
class CreateProblemsResponseDtoProblemsItem:
    """ An individual evaluation task — the core unit of work in the platform.

        Attributes:
            id (UUID): Stable problem identifier (UUID).
            environment_id (UUID): Environment this problem belongs to.
            external_id (None | str): Caller-provided external identifier for this problem. Null when no external system
                tracks it.
            is_template (bool): True for environment-scoped seed problems used as templates; false for regular problems.
                Templates are hidden from public lists and rejected by mutation routes.
            created_at (datetime.datetime): Timestamp when the problem was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the problem was last updated (ISO-8601, UTC).
            title (None | str | Unset): Human-readable problem title shown in lists and detail views.
            description (None | str | Unset): Free-text description of the problem. Null when unset.
            domain (None | str | Unset): Problem domain (e.g. the subject area the task belongs to). Null when unset.
     """

    id: UUID
    environment_id: UUID
    external_id: None | str
    is_template: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    title: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    domain: None | str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        environment_id = str(self.environment_id)

        external_id: None | str
        external_id = self.external_id

        is_template = self.is_template

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        domain: None | str | Unset
        if isinstance(self.domain, Unset):
            domain = UNSET
        else:
            domain = self.domain


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "environmentId": environment_id,
            "externalId": external_id,
            "isTemplate": is_template,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if domain is not UNSET:
            field_dict["domain"] = domain

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        environment_id = UUID(d.pop("environmentId"))




        def _parse_external_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_id = _parse_external_id(d.pop("externalId"))


        is_template = d.pop("isTemplate")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))


        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))


        def _parse_domain(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        domain = _parse_domain(d.pop("domain", UNSET))


        create_problems_response_dto_problems_item = cls(
            id=id,
            environment_id=environment_id,
            external_id=external_id,
            is_template=is_template,
            created_at=created_at,
            updated_at=updated_at,
            title=title,
            description=description,
            domain=domain,
        )

        return create_problems_response_dto_problems_item

