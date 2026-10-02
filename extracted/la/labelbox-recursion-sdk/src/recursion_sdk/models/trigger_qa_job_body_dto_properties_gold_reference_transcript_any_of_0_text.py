from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_text_kind import TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0TextKind






T = TypeVar("T", bound="TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0Text")



@_attrs_define
class TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0Text:
    """ Inline gold reference transcript supplied directly as text.

        Attributes:
            kind (TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0TextKind): Discriminator: inline gold reference
                transcript text.
            content (str): Inline gold reference transcript content.
     """

    kind: TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0TextKind
    content: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        content = self.content


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kind": kind,
            "content": content,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0TextKind(d.pop("kind"))




        content = d.pop("content")

        trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_text = cls(
            kind=kind,
            content=content,
        )


        trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_text.additional_properties = d
        return trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_text

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
