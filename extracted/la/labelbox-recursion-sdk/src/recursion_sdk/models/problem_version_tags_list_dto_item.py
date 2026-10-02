from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.problem_version_tags_list_dto_item_tags_item import ProblemVersionTagsListDtoItemTagsItem





T = TypeVar("T", bound="ProblemVersionTagsListDtoItem")



@_attrs_define
class ProblemVersionTagsListDtoItem:
    """ Tags applied to a single problem version.

        Attributes:
            problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have many versions; this
                points at one specific version.
            tags (list[ProblemVersionTagsListDtoItemTagsItem]): Tags currently applied to this problem version.
     """

    problem_version_id: UUID
    tags: list[ProblemVersionTagsListDtoItemTagsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_version_tags_list_dto_item_tags_item import ProblemVersionTagsListDtoItemTagsItem # noqa: PLC0415
        problem_version_id = str(self.problem_version_id)

        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "problemVersionId": problem_version_id,
            "tags": tags,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_version_tags_list_dto_item_tags_item import ProblemVersionTagsListDtoItemTagsItem # noqa: PLC0415
        d = dict(src_dict)
        problem_version_id = UUID(d.pop("problemVersionId"))




        tags = []
        _tags = d.pop("tags")
        for tags_item_data in (_tags):
            tags_item = ProblemVersionTagsListDtoItemTagsItem.from_dict(tags_item_data)



            tags.append(tags_item)


        problem_version_tags_list_dto_item = cls(
            problem_version_id=problem_version_id,
            tags=tags,
        )

        return problem_version_tags_list_dto_item

