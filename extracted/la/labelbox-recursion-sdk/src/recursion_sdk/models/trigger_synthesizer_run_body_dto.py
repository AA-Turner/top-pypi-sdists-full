from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.trigger_synthesizer_run_body_dto_built_in_key import TriggerSynthesizerRunBodyDtoBuiltInKey
from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="TriggerSynthesizerRunBodyDto")



@_attrs_define
class TriggerSynthesizerRunBodyDto:
    """ Payload for triggering a synthesizer run. Must set exactly one of the synthesizer job id (user-defined) or built-in
    key (built-in).

        Example:
            {'synthesizerJobId': 'b45c081d-3069-4e32-98d4-aa5ec3d442c6'}

        Attributes:
            synthesizer_job_id (UUID | Unset): Stable synthesizer-job identifier (UUID).
            built_in_key (TriggerSynthesizerRunBodyDtoBuiltInKey | Unset): Stable string key identifying a hardcoded built-
                in synthesizer.
     """

    synthesizer_job_id: UUID | Unset = UNSET
    built_in_key: TriggerSynthesizerRunBodyDtoBuiltInKey | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        synthesizer_job_id: str | Unset = UNSET
        if not isinstance(self.synthesizer_job_id, Unset):
            synthesizer_job_id = str(self.synthesizer_job_id)

        built_in_key: str | Unset = UNSET
        if not isinstance(self.built_in_key, Unset):
            built_in_key = self.built_in_key.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if synthesizer_job_id is not UNSET:
            field_dict["synthesizerJobId"] = synthesizer_job_id
        if built_in_key is not UNSET:
            field_dict["builtInKey"] = built_in_key

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _synthesizer_job_id = d.pop("synthesizerJobId", UNSET)
        synthesizer_job_id: UUID | Unset
        if isinstance(_synthesizer_job_id,  Unset):
            synthesizer_job_id = UNSET
        else:
            synthesizer_job_id = UUID(_synthesizer_job_id)




        _built_in_key = d.pop("builtInKey", UNSET)
        built_in_key: TriggerSynthesizerRunBodyDtoBuiltInKey | Unset
        if isinstance(_built_in_key,  Unset):
            built_in_key = UNSET
        else:
            built_in_key = TriggerSynthesizerRunBodyDtoBuiltInKey(_built_in_key)




        trigger_synthesizer_run_body_dto = cls(
            synthesizer_job_id=synthesizer_job_id,
            built_in_key=built_in_key,
        )


        trigger_synthesizer_run_body_dto.additional_properties = d
        return trigger_synthesizer_run_body_dto

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
