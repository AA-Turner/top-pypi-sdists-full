from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.run_config_version_dto_probe_files_item import RunConfigVersionDtoProbeFilesItem





T = TypeVar("T", bound="RunConfigVersionDtoProbe")



@_attrs_define
class RunConfigVersionDtoProbe:
    """ Probe spec used to verify this version before locking. Edits to this field clear the verification timestamp and the
    most-recent probe pointer.

        Attributes:
            prompt (str): Deterministic stdin handed to the agent when the probe runs. The verifier judges the resulting
                transcript against the quality check.
            files (list[RunConfigVersionDtoProbeFilesItem]): Optional additional input files staged alongside the prompt,
                used for harness-specific fixtures.
            quality_check (str | Unset): Plain-English description of what a passing transcript looks like, fed to the LLM
                judge. Falls back to "Agent responded with the correct answer" when omitted.
     """

    prompt: str
    files: list[RunConfigVersionDtoProbeFilesItem]
    quality_check: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_config_version_dto_probe_files_item import RunConfigVersionDtoProbeFilesItem # noqa: PLC0415
        prompt = self.prompt

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)



        quality_check = self.quality_check


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "prompt": prompt,
            "files": files,
        })
        if quality_check is not UNSET:
            field_dict["qualityCheck"] = quality_check

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_config_version_dto_probe_files_item import RunConfigVersionDtoProbeFilesItem # noqa: PLC0415
        d = dict(src_dict)
        prompt = d.pop("prompt")

        files = []
        _files = d.pop("files")
        for files_item_data in (_files):
            files_item = RunConfigVersionDtoProbeFilesItem.from_dict(files_item_data)



            files.append(files_item)


        quality_check = d.pop("qualityCheck", UNSET)

        run_config_version_dto_probe = cls(
            prompt=prompt,
            files=files,
            quality_check=quality_check,
        )

        return run_config_version_dto_probe

