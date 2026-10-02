from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_run_config_response_dto_run_config import CreateRunConfigResponseDtoRunConfig





T = TypeVar("T", bound="CreateRunConfigResponseDto")



@_attrs_define
class CreateRunConfigResponseDto:
    """ Response returned after creating a run config together with its initial draft version.

        Example:
            {'runConfig': {'id': '48eabce5-62a9-4356-9614-2de7d1b487a3', 'scope': {'level': 'env', 'id':
                '784e2386-e297-4f9d-a886-838422383b65'}, 'type': 'agent-harness', 'name': 'claude-sonnet-baseline',
                'description': 'Baseline Claude Sonnet solver harness for the vision-agent-eval environment.',
                'defaultRunConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad', 'tags': ['baseline'], 'createdByUserId':
                '49dea803-7390-49c4-abb1-5629718fc9cd', 'updatedByUserId': '49dea803-7390-49c4-abb1-5629718fc9cd', 'createdAt':
                '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-16T14:20:00.000Z'}, 'initialVersionId':
                '39088cb6-ca62-4544-a074-fc66e10807ad'}

        Attributes:
            run_config (CreateRunConfigResponseDtoRunConfig): The newly-created run config.
            initial_version_id (UUID): Identifier of the draft version created alongside the run config.
     """

    run_config: CreateRunConfigResponseDtoRunConfig
    initial_version_id: UUID





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_run_config_response_dto_run_config import CreateRunConfigResponseDtoRunConfig # noqa: PLC0415
        run_config = self.run_config.to_dict()

        initial_version_id = str(self.initial_version_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "runConfig": run_config,
            "initialVersionId": initial_version_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_run_config_response_dto_run_config import CreateRunConfigResponseDtoRunConfig # noqa: PLC0415
        d = dict(src_dict)
        run_config = CreateRunConfigResponseDtoRunConfig.from_dict(d.pop("runConfig"))




        initial_version_id = UUID(d.pop("initialVersionId"))




        create_run_config_response_dto = cls(
            run_config=run_config,
            initial_version_id=initial_version_id,
        )

        return create_run_config_response_dto

