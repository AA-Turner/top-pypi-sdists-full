from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsBoardOutcome")



@_attrs_define
class ManagedAgentsBoardOutcome:
    """ What a done task produced: the owner's summary, its confidence, and the artifact paths a reader or reviewer can
    open.

        Example:
            {'artifacts': ['example'], 'confidence': 'example', 'summary': 'example'}

        Attributes:
            summary (str): What the task produced, written by its owner when marking it done.
            artifacts (list[str] | Unset): Sandbox paths of the outputs the task produced, when the owner named them on
                completion.
            confidence (str | Unset): The owner's confidence in the result: low, medium, or high.
     """

    summary: str
    artifacts: list[str] | Unset = UNSET
    confidence: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        summary = self.summary

        artifacts: list[str] | Unset = UNSET
        if not isinstance(self.artifacts, Unset):
            artifacts = self.artifacts



        confidence = self.confidence


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "summary": summary,
        })
        if artifacts is not UNSET:
            field_dict["artifacts"] = artifacts
        if confidence is not UNSET:
            field_dict["confidence"] = confidence

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        summary = d.pop("summary")

        artifacts = cast(list[str], d.pop("artifacts", UNSET))


        confidence = d.pop("confidence", UNSET)

        managed_agents_board_outcome = cls(
            summary=summary,
            artifacts=artifacts,
            confidence=confidence,
        )


        managed_agents_board_outcome.additional_properties = d
        return managed_agents_board_outcome

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
