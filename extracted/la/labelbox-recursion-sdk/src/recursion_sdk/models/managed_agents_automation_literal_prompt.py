from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_literal_prompt_type import ManagedAgentsAutomationLiteralPromptType






T = TypeVar("T", bound="ManagedAgentsAutomationLiteralPrompt")



@_attrs_define
class ManagedAgentsAutomationLiteralPrompt:
    """ Literal initial prompt frozen onto each admitted automation run.

        Example:
            {'text': 'example', 'type': 'literal'}

        Attributes:
            text (str): Initial instruction supplied to every admitted run.
            type_ (ManagedAgentsAutomationLiteralPromptType): Literal prompt text with no interpolation.
     """

    text: str
    type_: ManagedAgentsAutomationLiteralPromptType





    def to_dict(self) -> dict[str, Any]:
        text = self.text

        type_ = self.type_.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "text": text,
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        text = d.pop("text")

        type_ = ManagedAgentsAutomationLiteralPromptType(d.pop("type"))




        managed_agents_automation_literal_prompt = cls(
            text=text,
            type_=type_,
        )

        return managed_agents_automation_literal_prompt

