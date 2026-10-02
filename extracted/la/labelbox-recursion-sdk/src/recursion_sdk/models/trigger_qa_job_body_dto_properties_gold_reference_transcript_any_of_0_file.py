from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_file_kind import TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0FileKind
from uuid import UUID






T = TypeVar("T", bound="TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0File")



@_attrs_define
class TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0File:
    """ Gold reference transcript supplied as an uploaded file reference.

        Attributes:
            kind (TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0FileKind): Discriminator: gold reference
                transcript by file id.
            file_id (UUID): Identifier of the uploaded gold reference transcript file.
     """

    kind: TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0FileKind
    file_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        file_id = str(self.file_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kind": kind,
            "fileId": file_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0FileKind(d.pop("kind"))




        file_id = UUID(d.pop("fileId"))




        trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_file = cls(
            kind=kind,
            file_id=file_id,
        )


        trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_file.additional_properties = d
        return trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_file

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
