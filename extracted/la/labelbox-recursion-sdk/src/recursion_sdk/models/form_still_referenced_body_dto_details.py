from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="FormStillReferencedBodyDtoDetails")



@_attrs_define
class FormStillReferencedBodyDtoDetails:
    """ Environment and problem identifiers that must release the form before it can be detached.

        Attributes:
            environment_ids (list[str]): Identifiers of environments that still reference the form bundle.
            problem_ids (list[str]): Identifiers of problems that still reference the form bundle.
     """

    environment_ids: list[str]
    problem_ids: list[str]





    def to_dict(self) -> dict[str, Any]:
        environment_ids = self.environment_ids



        problem_ids = self.problem_ids




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "environmentIds": environment_ids,
            "problemIds": problem_ids,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        environment_ids = cast(list[str], d.pop("environmentIds"))


        problem_ids = cast(list[str], d.pop("problemIds"))


        form_still_referenced_body_dto_details = cls(
            environment_ids=environment_ids,
            problem_ids=problem_ids,
        )

        return form_still_referenced_body_dto_details

