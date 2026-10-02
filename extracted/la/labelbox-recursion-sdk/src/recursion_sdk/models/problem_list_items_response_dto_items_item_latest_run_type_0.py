from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_list_items_response_dto_items_item_latest_run_type_0_status import ProblemListItemsResponseDtoItemsItemLatestRunType0Status
from typing import cast






T = TypeVar("T", bound="ProblemListItemsResponseDtoItemsItemLatestRunType0")



@_attrs_define
class ProblemListItemsResponseDtoItemsItemLatestRunType0:
    """ Summary of the most recent run attached to a problem, embedded in list responses.

        Attributes:
            status (ProblemListItemsResponseDtoItemsItemLatestRunType0Status): Lifecycle status of the latest run for this
                problem.
            final_score (float | None): Final grader score for the latest run. Null when the run has not been graded.
            api_model_name (None | str): Model that produced the latest run. Null when no model was recorded.
            prompt_excerpt (None | str): Truncated excerpt of the prompt used by the latest run, capped to
                PROMPT_EXCERPT_MAX_CHARS.
     """

    status: ProblemListItemsResponseDtoItemsItemLatestRunType0Status
    final_score: float | None
    api_model_name: None | str
    prompt_excerpt: None | str





    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        final_score: float | None
        final_score = self.final_score

        api_model_name: None | str
        api_model_name = self.api_model_name

        prompt_excerpt: None | str
        prompt_excerpt = self.prompt_excerpt


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
            "finalScore": final_score,
            "apiModelName": api_model_name,
            "promptExcerpt": prompt_excerpt,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = ProblemListItemsResponseDtoItemsItemLatestRunType0Status(d.pop("status"))




        def _parse_final_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        final_score = _parse_final_score(d.pop("finalScore"))


        def _parse_api_model_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        api_model_name = _parse_api_model_name(d.pop("apiModelName"))


        def _parse_prompt_excerpt(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        prompt_excerpt = _parse_prompt_excerpt(d.pop("promptExcerpt"))


        problem_list_items_response_dto_items_item_latest_run_type_0 = cls(
            status=status,
            final_score=final_score,
            api_model_name=api_model_name,
            prompt_excerpt=prompt_excerpt,
        )

        return problem_list_items_response_dto_items_item_latest_run_type_0

