from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="GenerateTitleResponseDto")



@_attrs_define
class GenerateTitleResponseDto:
    """ Response payload from the LLM title-suggestion endpoint.

        Attributes:
            suggestion (None | str): Suggested title for the problem produced by the LLM. Null when no suggestion could be
                generated.
     """

    suggestion: None | str





    def to_dict(self) -> dict[str, Any]:
        suggestion: None | str
        suggestion = self.suggestion


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "suggestion": suggestion,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_suggestion(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        suggestion = _parse_suggestion(d.pop("suggestion"))


        generate_title_response_dto = cls(
            suggestion=suggestion,
        )

        return generate_title_response_dto

