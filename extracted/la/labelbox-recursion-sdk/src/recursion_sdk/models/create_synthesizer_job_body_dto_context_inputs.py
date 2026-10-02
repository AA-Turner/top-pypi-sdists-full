from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_synthesizer_job_body_dto_context_inputs_current_field_values_item import CreateSynthesizerJobBodyDtoContextInputsCurrentFieldValuesItem
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_synthesizer_job_body_dto_context_inputs_files import CreateSynthesizerJobBodyDtoContextInputsFiles





T = TypeVar("T", bound="CreateSynthesizerJobBodyDtoContextInputs")



@_attrs_define
class CreateSynthesizerJobBodyDtoContextInputs:
    """ Declares which problem-version artifacts to bundle into the input tarball for the agent.

        Attributes:
            files (CreateSynthesizerJobBodyDtoContextInputsFiles): File buckets to include in the synthesizer input tarball.
            rubrics (bool): When true, include the problem version current rubrics in the input tarball.
            current_field_values (list[CreateSynthesizerJobBodyDtoContextInputsCurrentFieldValuesItem]): Existing problem-
                version field values to copy into the manifest so the synthesizer can condition on them.
            forms (bool | Unset): When true, include the active form schema and current answers in the manifest. Defaults to
                false for backward compatibility. Default: False.
     """

    files: CreateSynthesizerJobBodyDtoContextInputsFiles
    rubrics: bool
    current_field_values: list[CreateSynthesizerJobBodyDtoContextInputsCurrentFieldValuesItem]
    forms: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_synthesizer_job_body_dto_context_inputs_files import CreateSynthesizerJobBodyDtoContextInputsFiles # noqa: PLC0415
        files = self.files.to_dict()

        rubrics = self.rubrics

        current_field_values = []
        for current_field_values_item_data in self.current_field_values:
            current_field_values_item = current_field_values_item_data.value
            current_field_values.append(current_field_values_item)



        forms = self.forms


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "files": files,
            "rubrics": rubrics,
            "currentFieldValues": current_field_values,
        })
        if forms is not UNSET:
            field_dict["forms"] = forms

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_synthesizer_job_body_dto_context_inputs_files import CreateSynthesizerJobBodyDtoContextInputsFiles # noqa: PLC0415
        d = dict(src_dict)
        files = CreateSynthesizerJobBodyDtoContextInputsFiles.from_dict(d.pop("files"))




        rubrics = d.pop("rubrics")

        current_field_values = []
        _current_field_values = d.pop("currentFieldValues")
        for current_field_values_item_data in (_current_field_values):
            current_field_values_item = CreateSynthesizerJobBodyDtoContextInputsCurrentFieldValuesItem(current_field_values_item_data)



            current_field_values.append(current_field_values_item)


        forms = d.pop("forms", UNSET)

        create_synthesizer_job_body_dto_context_inputs = cls(
            files=files,
            rubrics=rubrics,
            current_field_values=current_field_values,
            forms=forms,
        )


        create_synthesizer_job_body_dto_context_inputs.additional_properties = d
        return create_synthesizer_job_body_dto_context_inputs

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
