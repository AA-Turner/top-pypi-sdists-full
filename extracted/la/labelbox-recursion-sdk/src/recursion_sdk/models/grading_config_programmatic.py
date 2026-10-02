from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.grading_config_programmatic_output_format import GradingConfigProgrammaticOutputFormat
from ..models.grading_config_programmatic_type import GradingConfigProgrammaticType
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="GradingConfigProgrammatic")



@_attrs_define
class GradingConfigProgrammatic:
    """ Grading config leaf that grades the run by executing a shell command in a sandboxed grader container.

        Attributes:
            type_ (GradingConfigProgrammaticType): Discriminator: grade by running a shell command inside a sandboxed
                container.
            command (str): Shell command executed inside the grader container to produce a score.
            output_format (GradingConfigProgrammaticOutputFormat): Format the grader command writes to stdout, used to parse
                the score.
            grader_image (None | str | Unset): Custom grader container image; null/undefined uses the platform default
                image.
     """

    type_: GradingConfigProgrammaticType
    command: str
    output_format: GradingConfigProgrammaticOutputFormat
    grader_image: None | str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        command = self.command

        output_format = self.output_format.value

        grader_image: None | str | Unset
        if isinstance(self.grader_image, Unset):
            grader_image = UNSET
        else:
            grader_image = self.grader_image


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
            "command": command,
            "outputFormat": output_format,
        })
        if grader_image is not UNSET:
            field_dict["graderImage"] = grader_image

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = GradingConfigProgrammaticType(d.pop("type"))




        command = d.pop("command")

        output_format = GradingConfigProgrammaticOutputFormat(d.pop("outputFormat"))




        def _parse_grader_image(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        grader_image = _parse_grader_image(d.pop("graderImage", UNSET))


        grading_config_programmatic = cls(
            type_=type_,
            command=command,
            output_format=output_format,
            grader_image=grader_image,
        )

        return grading_config_programmatic

