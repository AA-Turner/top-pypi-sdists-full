from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.grading_config_agentic_type import GradingConfigAgenticType






T = TypeVar("T", bound="GradingConfigAgentic")



@_attrs_define
class GradingConfigAgentic:
    """ Grading config leaf that grades the run via an LLM judge prompt.

        Attributes:
            type_ (GradingConfigAgenticType): Discriminator: grade with an LLM judge using a custom prompt.
            agentic_grading_prompt (str): Prompt sent to the LLM judge to produce a score for the run.
     """

    type_: GradingConfigAgenticType
    agentic_grading_prompt: str





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        agentic_grading_prompt = self.agentic_grading_prompt


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
            "agenticGradingPrompt": agentic_grading_prompt,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = GradingConfigAgenticType(d.pop("type"))




        agentic_grading_prompt = d.pop("agenticGradingPrompt")

        grading_config_agentic = cls(
            type_=type_,
            agentic_grading_prompt=agentic_grading_prompt,
        )

        return grading_config_agentic

