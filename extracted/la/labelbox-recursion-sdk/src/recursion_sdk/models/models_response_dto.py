from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ModelsResponseDto")



@_attrs_define
class ModelsResponseDto:
    """ List of model identifiers available for use as solver or grader models.

        Example:
            {'models': ['claude-opus-4-6', 'claude-sonnet-4-6', 'claude-opus-4-5-20251101', 'claude-sonnet-4-5-20250929',
                'claude-haiku-4-5-20251001']}

        Attributes:
            models (list[str]): Model identifiers available for routing solver and grader runs.
     """

    models: list[str]





    def to_dict(self) -> dict[str, Any]:
        models = self.models




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "models": models,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        models = cast(list[str], d.pop("models"))


        models_response_dto = cls(
            models=models,
        )

        return models_response_dto

