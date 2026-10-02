from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_run_config_dto_type import CreateRunConfigDtoType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_run_config_dto_config import CreateRunConfigDtoConfig
  from ..models.create_run_config_dto_properties_scope_env import CreateRunConfigDtoPropertiesScopeEnv
  from ..models.create_run_config_dto_properties_scope_org import CreateRunConfigDtoPropertiesScopeOrg
  from ..models.create_run_config_dto_properties_scope_problem import CreateRunConfigDtoPropertiesScopeProblem
  from ..models.create_run_config_dto_properties_scope_system import CreateRunConfigDtoPropertiesScopeSystem





T = TypeVar("T", bound="CreateRunConfigDto")



@_attrs_define
class CreateRunConfigDto:
    """ Input for creating a new run-config identity (and its v1 draft) at a chosen scope.

        Example:
            {'scope': {'level': 'env', 'id': '784e2386-e297-4f9d-a886-838422383b65'}, 'type': 'agent-harness', 'name':
                'claude-sonnet-baseline', 'description': 'Baseline Claude Sonnet solver harness for the vision-agent-eval
                environment.', 'config': {'harnessImageUrl': 'us-central1-docker.pkg.dev/lb-ml-prod/agent-service/claude-
                code:v1.2.3', 'containerSize': 'medium', 'args': '--max-turns 30', 'envVars': {'MODEL': 'claude-sonnet-4-6',
                'LOG_LEVEL': 'info'}, 'customerSecrets': [{'envVarName': 'ANTHROPIC_API_KEY'}], 'timeoutSeconds': 600,
                'mcpTools': [{'name': 'read_file', 'description': 'Read a file from the workspace.', 'service': 'worldsim',
                'category': 'filesystem', 'sortOrder': 10, 'readOnly': True, 'timeout': 30, 'inputSchema':
                '{"type":"object","properties":{"path":{"type":"string"}}}', 'serviceLabel': 'WorldSim'}]}}

        Attributes:
            scope (CreateRunConfigDtoPropertiesScopeEnv | CreateRunConfigDtoPropertiesScopeOrg |
                CreateRunConfigDtoPropertiesScopeProblem | CreateRunConfigDtoPropertiesScopeSystem): Scope this new run-config
                identity lives at. Determines which environments / problems can see and bind it.
            type_ (CreateRunConfigDtoType): Identity-level type. When forking from a parent, must match the parent run-
                config's type — cross-type forking is rejected.
            name (str): Human-readable display name.
            description (None | str | Unset): Free-form description. Send null or omit to leave empty.
            config (CreateRunConfigDtoConfig | Unset): Optional initial payload for the v1 draft. When omitted, v1 is
                created with an empty config; supply a parent run-config version id to seed from another version instead.
            parent_run_config_version_id (UUID | Unset): Source version to seed v1 from (config, probe, attachments). For
                agent-harness configs the parent must be locked; snapshot configs also accept drafts.
            tags (list[str] | Unset): Free-form tags for list filtering. Omit to leave the run config untagged.
     """

    scope: CreateRunConfigDtoPropertiesScopeEnv | CreateRunConfigDtoPropertiesScopeOrg | CreateRunConfigDtoPropertiesScopeProblem | CreateRunConfigDtoPropertiesScopeSystem
    type_: CreateRunConfigDtoType
    name: str
    description: None | str | Unset = UNSET
    config: CreateRunConfigDtoConfig | Unset = UNSET
    parent_run_config_version_id: UUID | Unset = UNSET
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_run_config_dto_config import CreateRunConfigDtoConfig # noqa: PLC0415
        from ..models.create_run_config_dto_properties_scope_env import CreateRunConfigDtoPropertiesScopeEnv # noqa: PLC0415
        from ..models.create_run_config_dto_properties_scope_org import CreateRunConfigDtoPropertiesScopeOrg # noqa: PLC0415
        from ..models.create_run_config_dto_properties_scope_problem import CreateRunConfigDtoPropertiesScopeProblem # noqa: PLC0415
        from ..models.create_run_config_dto_properties_scope_system import CreateRunConfigDtoPropertiesScopeSystem # noqa: PLC0415
        scope: dict[str, Any]
        if isinstance(self.scope, CreateRunConfigDtoPropertiesScopeSystem):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, CreateRunConfigDtoPropertiesScopeOrg):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, CreateRunConfigDtoPropertiesScopeEnv):
            scope = self.scope.to_dict()
        else:
            scope = self.scope.to_dict()


        type_ = self.type_.value

        name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        parent_run_config_version_id: str | Unset = UNSET
        if not isinstance(self.parent_run_config_version_id, Unset):
            parent_run_config_version_id = str(self.parent_run_config_version_id)

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "scope": scope,
            "type": type_,
            "name": name,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if config is not UNSET:
            field_dict["config"] = config
        if parent_run_config_version_id is not UNSET:
            field_dict["parentRunConfigVersionId"] = parent_run_config_version_id
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_run_config_dto_config import CreateRunConfigDtoConfig # noqa: PLC0415
        from ..models.create_run_config_dto_properties_scope_env import CreateRunConfigDtoPropertiesScopeEnv # noqa: PLC0415
        from ..models.create_run_config_dto_properties_scope_org import CreateRunConfigDtoPropertiesScopeOrg # noqa: PLC0415
        from ..models.create_run_config_dto_properties_scope_problem import CreateRunConfigDtoPropertiesScopeProblem # noqa: PLC0415
        from ..models.create_run_config_dto_properties_scope_system import CreateRunConfigDtoPropertiesScopeSystem # noqa: PLC0415
        d = dict(src_dict)
        def _parse_scope(data: object) -> CreateRunConfigDtoPropertiesScopeEnv | CreateRunConfigDtoPropertiesScopeOrg | CreateRunConfigDtoPropertiesScopeProblem | CreateRunConfigDtoPropertiesScopeSystem:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_0 = CreateRunConfigDtoPropertiesScopeSystem.from_dict(data)



                return scope_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_1 = CreateRunConfigDtoPropertiesScopeOrg.from_dict(data)



                return scope_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_2 = CreateRunConfigDtoPropertiesScopeEnv.from_dict(data)



                return scope_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            scope_type_3 = CreateRunConfigDtoPropertiesScopeProblem.from_dict(data)



            return scope_type_3

        scope = _parse_scope(d.pop("scope"))


        type_ = CreateRunConfigDtoType(d.pop("type"))




        name = d.pop("name")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))


        _config = d.pop("config", UNSET)
        config: CreateRunConfigDtoConfig | Unset
        if isinstance(_config,  Unset):
            config = UNSET
        else:
            config = CreateRunConfigDtoConfig.from_dict(_config)




        _parent_run_config_version_id = d.pop("parentRunConfigVersionId", UNSET)
        parent_run_config_version_id: UUID | Unset
        if isinstance(_parent_run_config_version_id,  Unset):
            parent_run_config_version_id = UNSET
        else:
            parent_run_config_version_id = UUID(_parent_run_config_version_id)




        tags = cast(list[str], d.pop("tags", UNSET))


        create_run_config_dto = cls(
            scope=scope,
            type_=type_,
            name=name,
            description=description,
            config=config,
            parent_run_config_version_id=parent_run_config_version_id,
            tags=tags,
        )


        create_run_config_dto.additional_properties = d
        return create_run_config_dto

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
