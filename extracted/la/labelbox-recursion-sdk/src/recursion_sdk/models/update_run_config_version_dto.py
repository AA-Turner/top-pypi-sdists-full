from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.update_run_config_version_dto_config import UpdateRunConfigVersionDtoConfig
  from ..models.update_run_config_version_dto_config_schema_type_0 import UpdateRunConfigVersionDtoConfigSchemaType0
  from ..models.update_run_config_version_dto_config_template_type_0 import UpdateRunConfigVersionDtoConfigTemplateType0
  from ..models.update_run_config_version_dto_probe import UpdateRunConfigVersionDtoProbe





T = TypeVar("T", bound="UpdateRunConfigVersionDto")



@_attrs_define
class UpdateRunConfigVersionDto:
    """ Patch-style update body for a run-config version. Only draft versions are mutable; locked versions reject all
    updates.

        Example:
            {'config': {'harnessImageUrl': 'us-central1-docker.pkg.dev/lb-ml-prod/agent-service/claude-code:v1.2.3',
                'containerSize': 'medium', 'args': '--max-turns 30', 'envVars': {'MODEL': 'claude-sonnet-4-6', 'LOG_LEVEL':
                'info'}, 'customerSecrets': [{'envVarName': 'ANTHROPIC_API_KEY'}], 'timeoutSeconds': 600, 'mcpTools': [{'name':
                'read_file', 'description': 'Read a file from the workspace.', 'service': 'worldsim', 'category': 'filesystem',
                'sortOrder': 10, 'readOnly': True, 'timeout': 30, 'inputSchema':
                '{"type":"object","properties":{"path":{"type":"string"}}}', 'serviceLabel': 'WorldSim'}]}, 'probe': {'prompt':
                'Inspect the attached image and report whether a surface defect is visible.', 'files': [], 'qualityCheck':
                'Agent identifies the surface defect and reports its location.'}, 'notes': 'Raised --max-turns to 30 after the
                v2 probe ran out of turns.'}

        Attributes:
            config (UpdateRunConfigVersionDtoConfig | Unset): New payload. Editing this on a draft clears the verification
                timestamp and the most-recent probe pointer. Omit to leave unchanged.
            config_template (None | Unset | UpdateRunConfigVersionDtoConfigTemplateType0): New container-authored default
                config template. Send null to clear; omit to leave unchanged.
            config_schema (None | Unset | UpdateRunConfigVersionDtoConfigSchemaType0): New container-authored config JSON
                Schema. Send null to clear; omit to leave unchanged.
            probe (UpdateRunConfigVersionDtoProbe | Unset): New probe spec. Editing this on a draft clears the verification
                timestamp and the most-recent probe pointer. Omit to leave unchanged.
            notes (None | str | Unset): New notes. Send null to clear; omit to leave unchanged.
     """

    config: UpdateRunConfigVersionDtoConfig | Unset = UNSET
    config_template: None | Unset | UpdateRunConfigVersionDtoConfigTemplateType0 = UNSET
    config_schema: None | Unset | UpdateRunConfigVersionDtoConfigSchemaType0 = UNSET
    probe: UpdateRunConfigVersionDtoProbe | Unset = UNSET
    notes: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.update_run_config_version_dto_config import UpdateRunConfigVersionDtoConfig # noqa: PLC0415
        from ..models.update_run_config_version_dto_config_schema_type_0 import UpdateRunConfigVersionDtoConfigSchemaType0 # noqa: PLC0415
        from ..models.update_run_config_version_dto_config_template_type_0 import UpdateRunConfigVersionDtoConfigTemplateType0 # noqa: PLC0415
        from ..models.update_run_config_version_dto_probe import UpdateRunConfigVersionDtoProbe # noqa: PLC0415
        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        config_template: dict[str, Any] | None | Unset
        if isinstance(self.config_template, Unset):
            config_template = UNSET
        elif isinstance(self.config_template, UpdateRunConfigVersionDtoConfigTemplateType0):
            config_template = self.config_template.to_dict()
        else:
            config_template = self.config_template

        config_schema: dict[str, Any] | None | Unset
        if isinstance(self.config_schema, Unset):
            config_schema = UNSET
        elif isinstance(self.config_schema, UpdateRunConfigVersionDtoConfigSchemaType0):
            config_schema = self.config_schema.to_dict()
        else:
            config_schema = self.config_schema

        probe: dict[str, Any] | Unset = UNSET
        if not isinstance(self.probe, Unset):
            probe = self.probe.to_dict()

        notes: None | str | Unset
        if isinstance(self.notes, Unset):
            notes = UNSET
        else:
            notes = self.notes


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if config is not UNSET:
            field_dict["config"] = config
        if config_template is not UNSET:
            field_dict["configTemplate"] = config_template
        if config_schema is not UNSET:
            field_dict["configSchema"] = config_schema
        if probe is not UNSET:
            field_dict["probe"] = probe
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_run_config_version_dto_config import UpdateRunConfigVersionDtoConfig # noqa: PLC0415
        from ..models.update_run_config_version_dto_config_schema_type_0 import UpdateRunConfigVersionDtoConfigSchemaType0 # noqa: PLC0415
        from ..models.update_run_config_version_dto_config_template_type_0 import UpdateRunConfigVersionDtoConfigTemplateType0 # noqa: PLC0415
        from ..models.update_run_config_version_dto_probe import UpdateRunConfigVersionDtoProbe # noqa: PLC0415
        d = dict(src_dict)
        _config = d.pop("config", UNSET)
        config: UpdateRunConfigVersionDtoConfig | Unset
        if isinstance(_config,  Unset):
            config = UNSET
        else:
            config = UpdateRunConfigVersionDtoConfig.from_dict(_config)




        def _parse_config_template(data: object) -> None | Unset | UpdateRunConfigVersionDtoConfigTemplateType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                config_template_type_0 = UpdateRunConfigVersionDtoConfigTemplateType0.from_dict(data)



                return config_template_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UpdateRunConfigVersionDtoConfigTemplateType0, data)

        config_template = _parse_config_template(d.pop("configTemplate", UNSET))


        def _parse_config_schema(data: object) -> None | Unset | UpdateRunConfigVersionDtoConfigSchemaType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                config_schema_type_0 = UpdateRunConfigVersionDtoConfigSchemaType0.from_dict(data)



                return config_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UpdateRunConfigVersionDtoConfigSchemaType0, data)

        config_schema = _parse_config_schema(d.pop("configSchema", UNSET))


        _probe = d.pop("probe", UNSET)
        probe: UpdateRunConfigVersionDtoProbe | Unset
        if isinstance(_probe,  Unset):
            probe = UNSET
        else:
            probe = UpdateRunConfigVersionDtoProbe.from_dict(_probe)




        def _parse_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        notes = _parse_notes(d.pop("notes", UNSET))


        update_run_config_version_dto = cls(
            config=config,
            config_template=config_template,
            config_schema=config_schema,
            probe=probe,
            notes=notes,
        )


        update_run_config_version_dto.additional_properties = d
        return update_run_config_version_dto

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
