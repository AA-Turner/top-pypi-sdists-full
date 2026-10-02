from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.synthesizer_job_dto_context_inputs_current_field_values_item import SynthesizerJobDtoContextInputsCurrentFieldValuesItem
from typing import cast

if TYPE_CHECKING:
  from ..models.synthesizer_job_dto_context_inputs_files import SynthesizerJobDtoContextInputsFiles





T = TypeVar("T", bound="SynthesizerJobDtoContextInputs")



@_attrs_define
class SynthesizerJobDtoContextInputs:
    """ Declares which problem-version artifacts are bundled into the input tarball for the agent.

        Attributes:
            files (SynthesizerJobDtoContextInputsFiles): File buckets to include in the synthesizer input tarball.
            rubrics (bool): When true, include the problem version current rubrics in the input tarball.
            current_field_values (list[SynthesizerJobDtoContextInputsCurrentFieldValuesItem]): Existing problem-version
                field values to copy into the manifest so the synthesizer can condition on them.
            forms (bool): When true, include the active form schema and current answers in the manifest. Defaults to false
                for backward compatibility. Default: False.
     """

    files: SynthesizerJobDtoContextInputsFiles
    rubrics: bool
    current_field_values: list[SynthesizerJobDtoContextInputsCurrentFieldValuesItem]
    forms: bool = False





    def to_dict(self) -> dict[str, Any]:
        from ..models.synthesizer_job_dto_context_inputs_files import SynthesizerJobDtoContextInputsFiles # noqa: PLC0415
        files = self.files.to_dict()

        rubrics = self.rubrics

        current_field_values = []
        for current_field_values_item_data in self.current_field_values:
            current_field_values_item = current_field_values_item_data.value
            current_field_values.append(current_field_values_item)



        forms = self.forms


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "files": files,
            "rubrics": rubrics,
            "currentFieldValues": current_field_values,
            "forms": forms,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.synthesizer_job_dto_context_inputs_files import SynthesizerJobDtoContextInputsFiles # noqa: PLC0415
        d = dict(src_dict)
        files = SynthesizerJobDtoContextInputsFiles.from_dict(d.pop("files"))




        rubrics = d.pop("rubrics")

        current_field_values = []
        _current_field_values = d.pop("currentFieldValues")
        for current_field_values_item_data in (_current_field_values):
            current_field_values_item = SynthesizerJobDtoContextInputsCurrentFieldValuesItem(current_field_values_item_data)



            current_field_values.append(current_field_values_item)


        forms = d.pop("forms")

        synthesizer_job_dto_context_inputs = cls(
            files=files,
            rubrics=rubrics,
            current_field_values=current_field_values,
            forms=forms,
        )

        return synthesizer_job_dto_context_inputs

