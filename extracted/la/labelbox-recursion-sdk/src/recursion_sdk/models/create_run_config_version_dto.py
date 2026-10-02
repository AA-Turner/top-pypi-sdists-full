from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_run_config_version_dto_config import CreateRunConfigVersionDtoConfig
  from ..models.create_run_config_version_dto_probe import CreateRunConfigVersionDtoProbe





T = TypeVar("T", bound="CreateRunConfigVersionDto")



@_attrs_define
class CreateRunConfigVersionDto:
    """ Input for creating a new draft version under an existing run-config identity.

        Example:
            {'config': {'harnessImageUrl': 'us-central1-docker.pkg.dev/lb-ml-prod/agent-service/claude-code:v1.2.3',
                'containerSize': 'medium', 'args': '--max-turns 30', 'envVars': {'MODEL': 'claude-sonnet-4-6', 'LOG_LEVEL':
                'info'}, 'customerSecrets': [{'envVarName': 'ANTHROPIC_API_KEY'}], 'timeoutSeconds': 600, 'mcpTools': [{'name':
                'read_file', 'description': 'Read a file from the workspace.', 'service': 'worldsim', 'category': 'filesystem',
                'sortOrder': 10, 'readOnly': True, 'timeout': 30, 'inputSchema':
                '{"type":"object","properties":{"path":{"type":"string"}}}', 'serviceLabel': 'WorldSim'}]}, 'probe': {'prompt':
                'Inspect the attached image and report whether a surface defect is visible.', 'files': [], 'qualityCheck':
                'Agent identifies the surface defect and reports its location.'}, 'notes': 'Raised --max-turns to 30 after the
                v2 probe ran out of turns.', 'parentRunConfigVersionId': 'b2d6f3a1-4c8e-4a7b-9f10-2e5c6d8a1b40'}

        Attributes:
            config (CreateRunConfigVersionDtoConfig | Unset): Optional initial config for the new draft. When omitted, the
                draft is seeded from the parent version when provided, otherwise starts empty.
            probe (CreateRunConfigVersionDtoProbe | Unset): Optional initial probe spec. When omitted, falls back to
                platform defaults or the parent version's probe.
            notes (str | Unset): Free-form notes attached to the new version.
            parent_run_config_version_id (UUID | Unset): Locked version to seed the new draft from (config, probe,
                attachments). Must reference a locked version.
     """

    config: CreateRunConfigVersionDtoConfig | Unset = UNSET
    probe: CreateRunConfigVersionDtoProbe | Unset = UNSET
    notes: str | Unset = UNSET
    parent_run_config_version_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_run_config_version_dto_config import CreateRunConfigVersionDtoConfig # noqa: PLC0415
        from ..models.create_run_config_version_dto_probe import CreateRunConfigVersionDtoProbe # noqa: PLC0415
        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        probe: dict[str, Any] | Unset = UNSET
        if not isinstance(self.probe, Unset):
            probe = self.probe.to_dict()

        notes = self.notes

        parent_run_config_version_id: str | Unset = UNSET
        if not isinstance(self.parent_run_config_version_id, Unset):
            parent_run_config_version_id = str(self.parent_run_config_version_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if config is not UNSET:
            field_dict["config"] = config
        if probe is not UNSET:
            field_dict["probe"] = probe
        if notes is not UNSET:
            field_dict["notes"] = notes
        if parent_run_config_version_id is not UNSET:
            field_dict["parentRunConfigVersionId"] = parent_run_config_version_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_run_config_version_dto_config import CreateRunConfigVersionDtoConfig # noqa: PLC0415
        from ..models.create_run_config_version_dto_probe import CreateRunConfigVersionDtoProbe # noqa: PLC0415
        d = dict(src_dict)
        _config = d.pop("config", UNSET)
        config: CreateRunConfigVersionDtoConfig | Unset
        if isinstance(_config,  Unset):
            config = UNSET
        else:
            config = CreateRunConfigVersionDtoConfig.from_dict(_config)




        _probe = d.pop("probe", UNSET)
        probe: CreateRunConfigVersionDtoProbe | Unset
        if isinstance(_probe,  Unset):
            probe = UNSET
        else:
            probe = CreateRunConfigVersionDtoProbe.from_dict(_probe)




        notes = d.pop("notes", UNSET)

        _parent_run_config_version_id = d.pop("parentRunConfigVersionId", UNSET)
        parent_run_config_version_id: UUID | Unset
        if isinstance(_parent_run_config_version_id,  Unset):
            parent_run_config_version_id = UNSET
        else:
            parent_run_config_version_id = UUID(_parent_run_config_version_id)




        create_run_config_version_dto = cls(
            config=config,
            probe=probe,
            notes=notes,
            parent_run_config_version_id=parent_run_config_version_id,
        )


        create_run_config_version_dto.additional_properties = d
        return create_run_config_version_dto

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
