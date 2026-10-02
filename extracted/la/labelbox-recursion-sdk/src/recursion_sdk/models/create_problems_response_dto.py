from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.create_problems_response_dto_problems_item import CreateProblemsResponseDtoProblemsItem





T = TypeVar("T", bound="CreateProblemsResponseDto")



@_attrs_define
class CreateProblemsResponseDto:
    """ Response payload returned by the bulk problem-creation endpoint.

        Example:
            {'created': 1, 'problems': [{'id': '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'environmentId':
                '784e2386-e297-4f9d-a886-838422383b65', 'externalId': 'detect-surface-defects', 'title': 'Detect surface defects
                on machined parts', 'description': 'Given a photo of a machined part, identify visible surface defects.',
                'domain': 'manufacturing-qa', 'isTemplate': False, 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt':
                '2026-01-16T14:20:00.000Z'}]}

        Attributes:
            created (float): Number of problems created in this bulk request. Example: 12.
            problems (list[CreateProblemsResponseDtoProblemsItem]): Problems created by this request, in creation order.
     """

    created: float
    problems: list[CreateProblemsResponseDtoProblemsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_problems_response_dto_problems_item import CreateProblemsResponseDtoProblemsItem # noqa: PLC0415
        created = self.created

        problems = []
        for problems_item_data in self.problems:
            problems_item = problems_item_data.to_dict()
            problems.append(problems_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created": created,
            "problems": problems,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_problems_response_dto_problems_item import CreateProblemsResponseDtoProblemsItem # noqa: PLC0415
        d = dict(src_dict)
        created = d.pop("created")

        problems = []
        _problems = d.pop("problems")
        for problems_item_data in (_problems):
            problems_item = CreateProblemsResponseDtoProblemsItem.from_dict(problems_item_data)



            problems.append(problems_item)


        create_problems_response_dto = cls(
            created=created,
            problems=problems,
        )

        return create_problems_response_dto

