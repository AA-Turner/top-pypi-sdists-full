from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ProblemSummariesResponseDtoItemsItem")



@_attrs_define
class ProblemSummariesResponseDtoItemsItem:
    """ Minimal problem record without per-row aggregates, for high-fanout reads.

        Attributes:
            id (UUID): Stable problem identifier (UUID).
            external_id (None | str): Caller-provided external identifier for this problem. Null when no external system
                tracks it.
            title (None | str): Human-readable problem title shown in picker rows.
            has_locked_version (bool): True when the problem has at least one locked (immutable) version.
     """

    id: UUID
    external_id: None | str
    title: None | str
    has_locked_version: bool





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        external_id: None | str
        external_id = self.external_id

        title: None | str
        title = self.title

        has_locked_version = self.has_locked_version


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "externalId": external_id,
            "title": title,
            "hasLockedVersion": has_locked_version,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_external_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_id = _parse_external_id(d.pop("externalId"))


        def _parse_title(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        title = _parse_title(d.pop("title"))


        has_locked_version = d.pop("hasLockedVersion")

        problem_summaries_response_dto_items_item = cls(
            id=id,
            external_id=external_id,
            title=title,
            has_locked_version=has_locked_version,
        )

        return problem_summaries_response_dto_items_item

