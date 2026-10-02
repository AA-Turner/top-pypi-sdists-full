from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.resolved_run_config_dto_type import ResolvedRunConfigDtoType
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.resolved_run_config_dto_config import ResolvedRunConfigDtoConfig
  from ..models.resolved_run_config_dto_provenance import ResolvedRunConfigDtoProvenance





T = TypeVar("T", bound="ResolvedRunConfigDto")



@_attrs_define
class ResolvedRunConfigDto:
    """ Selected run-config version payload before consumer-specific defaults or inherited problem policy are applied,
    including provenance for the UI.

        Example:
            {'runConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad', 'runConfigId':
                '48eabce5-62a9-4356-9614-2de7d1b487a3', 'type': 'agent-harness', 'config': {'harnessImageUrl': 'us-
                central1-docker.pkg.dev/lb-ml-prod/agent-service/claude-code:v1.2.3', 'containerSize': 'medium', 'args': '--max-
                turns 30', 'envVars': {'MODEL': 'claude-sonnet-4-6', 'LOG_LEVEL': 'info'}, 'customerSecrets': [{'envVarName':
                'ANTHROPIC_API_KEY'}], 'timeoutSeconds': 600, 'mcpTools': [{'name': 'read_file', 'description': 'Read a file
                from the workspace.', 'service': 'worldsim', 'category': 'filesystem', 'sortOrder': 10, 'readOnly': True,
                'timeout': 30, 'inputSchema': '{"type":"object","properties":{"path":{"type":"string"}}}', 'serviceLabel':
                'WorldSim'}]}, 'provenance': {'runConfigId': '48eabce5-62a9-4356-9614-2de7d1b487a3', 'runConfigVersionId':
                '39088cb6-ca62-4544-a074-fc66e10807ad', 'runConfigName': 'claude-sonnet-baseline', 'scope': {'level': 'env',
                'id': '784e2386-e297-4f9d-a886-838422383b65'}, 'versionNumber': 3}}

        Attributes:
            run_config_version_id (UUID): Run-config version that produced the selected pre-consumer payload.
            run_config_id (UUID): Owning run-config identity.
            type_ (ResolvedRunConfigDtoType): Type discriminator copied from the owning identity. Submit-site dispatch
                switches on this so future types force every pipeline to add a case.
            provenance (ResolvedRunConfigDtoProvenance): Which run-config / version this resolved to, for "this run came
                from …" displays.
            config (ResolvedRunConfigDtoConfig): Selected version payload before consumer-specific defaults or inherited
                problem policy are applied. Shape is keyed by the run-config type.
     """

    run_config_version_id: UUID
    run_config_id: UUID
    type_: ResolvedRunConfigDtoType
    provenance: ResolvedRunConfigDtoProvenance
    config: ResolvedRunConfigDtoConfig





    def to_dict(self) -> dict[str, Any]:
        from ..models.resolved_run_config_dto_config import ResolvedRunConfigDtoConfig # noqa: PLC0415
        from ..models.resolved_run_config_dto_provenance import ResolvedRunConfigDtoProvenance # noqa: PLC0415
        run_config_version_id = str(self.run_config_version_id)

        run_config_id = str(self.run_config_id)

        type_ = self.type_.value

        provenance = self.provenance.to_dict()

        config = self.config.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "runConfigVersionId": run_config_version_id,
            "runConfigId": run_config_id,
            "type": type_,
            "provenance": provenance,
            "config": config,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resolved_run_config_dto_config import ResolvedRunConfigDtoConfig # noqa: PLC0415
        from ..models.resolved_run_config_dto_provenance import ResolvedRunConfigDtoProvenance # noqa: PLC0415
        d = dict(src_dict)
        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        run_config_id = UUID(d.pop("runConfigId"))




        type_ = ResolvedRunConfigDtoType(d.pop("type"))




        provenance = ResolvedRunConfigDtoProvenance.from_dict(d.pop("provenance"))




        config = ResolvedRunConfigDtoConfig.from_dict(d.pop("config"))




        resolved_run_config_dto = cls(
            run_config_version_id=run_config_version_id,
            run_config_id=run_config_id,
            type_=type_,
            provenance=provenance,
            config=config,
        )

        return resolved_run_config_dto

