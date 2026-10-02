from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AdminStatsDtoTokensByModelItem")



@_attrs_define
class AdminStatsDtoTokensByModelItem:
    """ Token usage for a single model.

        Attributes:
            model (str): LLM model identifier (e.g. provider/name).
            tokens (float): Total tokens consumed by this model across all runs.
     """

    model: str
    tokens: float





    def to_dict(self) -> dict[str, Any]:
        model = self.model

        tokens = self.tokens


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "model": model,
            "tokens": tokens,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model = d.pop("model")

        tokens = d.pop("tokens")

        admin_stats_dto_tokens_by_model_item = cls(
            model=model,
            tokens=tokens,
        )

        return admin_stats_dto_tokens_by_model_item

