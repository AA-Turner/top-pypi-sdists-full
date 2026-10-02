from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsOpenSessionAnalystRequest")



@_attrs_define
class ManagedAgentsOpenSessionAnalystRequest:
    """ Optional request body of openSessionAnalyst. An empty body returns the caller's conversation with the tree, if any;
    question asks (starting the conversation if needed); reset ends the current conversation.

        Example:
            {'question': 'example', 'reset': True}

        Attributes:
            question (str | Unset): A question for the analyst. Starts the caller's conversation with this tree when there
                is none, as its first turn; otherwise it is delivered to the existing conversation. An analyst is never started
                without one.
            reset (bool | Unset): When true, ends the caller's current conversation with this tree: the analyst session is
                cancelled and stays readable, and the caller has no conversation until the next question.
     """

    question: str | Unset = UNSET
    reset: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        question = self.question

        reset = self.reset


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if question is not UNSET:
            field_dict["question"] = question
        if reset is not UNSET:
            field_dict["reset"] = reset

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        question = d.pop("question", UNSET)

        reset = d.pop("reset", UNSET)

        managed_agents_open_session_analyst_request = cls(
            question=question,
            reset=reset,
        )


        managed_agents_open_session_analyst_request.additional_properties = d
        return managed_agents_open_session_analyst_request

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
