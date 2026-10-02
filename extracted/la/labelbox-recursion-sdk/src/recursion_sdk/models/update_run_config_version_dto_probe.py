from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.update_run_config_version_dto_probe_files_item import UpdateRunConfigVersionDtoProbeFilesItem





T = TypeVar("T", bound="UpdateRunConfigVersionDtoProbe")



@_attrs_define
class UpdateRunConfigVersionDtoProbe:
    """ New probe spec. Editing this on a draft clears the verification timestamp and the most-recent probe pointer. Omit to
    leave unchanged.

        Attributes:
            prompt (str): Deterministic stdin handed to the agent when the probe runs. The verifier judges the resulting
                transcript against the quality check.
            files (list[UpdateRunConfigVersionDtoProbeFilesItem] | Unset): Optional additional input files staged alongside
                the prompt, used for harness-specific fixtures.
            quality_check (str | Unset): Plain-English description of what a passing transcript looks like, fed to the LLM
                judge. Falls back to "Agent responded with the correct answer" when omitted.
     """

    prompt: str
    files: list[UpdateRunConfigVersionDtoProbeFilesItem] | Unset = UNSET
    quality_check: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.update_run_config_version_dto_probe_files_item import UpdateRunConfigVersionDtoProbeFilesItem # noqa: PLC0415
        prompt = self.prompt

        files: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)



        quality_check = self.quality_check


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "prompt": prompt,
        })
        if files is not UNSET:
            field_dict["files"] = files
        if quality_check is not UNSET:
            field_dict["qualityCheck"] = quality_check

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_run_config_version_dto_probe_files_item import UpdateRunConfigVersionDtoProbeFilesItem # noqa: PLC0415
        d = dict(src_dict)
        prompt = d.pop("prompt")

        _files = d.pop("files", UNSET)
        files: list[UpdateRunConfigVersionDtoProbeFilesItem] | Unset = UNSET
        if _files is not UNSET:
            files = []
            for files_item_data in _files:
                files_item = UpdateRunConfigVersionDtoProbeFilesItem.from_dict(files_item_data)



                files.append(files_item)


        quality_check = d.pop("qualityCheck", UNSET)

        update_run_config_version_dto_probe = cls(
            prompt=prompt,
            files=files,
            quality_check=quality_check,
        )


        update_run_config_version_dto_probe.additional_properties = d
        return update_run_config_version_dto_probe

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
