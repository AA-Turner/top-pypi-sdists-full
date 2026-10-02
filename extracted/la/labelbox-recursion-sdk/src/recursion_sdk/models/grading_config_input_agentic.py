from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.grading_config_input_agentic_type import GradingConfigInputAgenticType






T = TypeVar("T", bound="GradingConfigInputAgentic")



@_attrs_define
class GradingConfigInputAgentic:
    """ Grading config leaf that grades the run via an LLM judge prompt.

        Attributes:
            type_ (GradingConfigInputAgenticType): Discriminator: grade with an LLM judge using a custom prompt.
            agentic_grading_prompt (str): Prompt sent to the LLM judge to produce a score for the run.
     """

    type_: GradingConfigInputAgenticType
    agentic_grading_prompt: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        agentic_grading_prompt = self.agentic_grading_prompt


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "agenticGradingPrompt": agentic_grading_prompt,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = GradingConfigInputAgenticType(d.pop("type"))




        agentic_grading_prompt = d.pop("agenticGradingPrompt")

        grading_config_input_agentic = cls(
            type_=type_,
            agentic_grading_prompt=agentic_grading_prompt,
        )


        grading_config_input_agentic.additional_properties = d
        return grading_config_input_agentic

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
