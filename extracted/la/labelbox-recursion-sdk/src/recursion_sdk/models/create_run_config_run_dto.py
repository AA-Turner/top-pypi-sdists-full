from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_run_config_run_dto_completion_mode import CreateRunConfigRunDtoCompletionMode
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_run_config_run_dto_config import CreateRunConfigRunDtoConfig
  from ..models.create_run_config_run_dto_env import CreateRunConfigRunDtoEnv
  from ..models.create_run_config_run_dto_platform_aux_input import CreateRunConfigRunDtoPlatformAuxInput
  from ..models.create_run_config_run_dto_platform_input_refs import CreateRunConfigRunDtoPlatformInputRefs





T = TypeVar("T", bound="CreateRunConfigRunDto")



@_attrs_define
class CreateRunConfigRunDto:
    """ Public input for starting a generic run-config execution.

        Example:
            {'runConfigVersionId': '11111111-1111-4111-8111-111111111111', 'runName': 'generic-run', 'config': {}}

        Attributes:
            run_config_version_id (UUID): Locked, agent-harness type run-config version to execute. Re-resolved at submit
                time.
            run_name (str): Human-readable run name (platform-input run_name).
            config (CreateRunConfigRunDtoConfig): Opaque trainer config blob — never inspected by the platform (B7).
            timeout_seconds (int | Unset): Wall-clock container timeout override. Omit to use the run-config version's own
                timeoutSeconds.
            platform_input_refs (CreateRunConfigRunDtoPlatformInputRefs | Unset): Additional platform-owned top-level fields
                a composing parent (e.g. tuning_run) merges into the platform-input envelope alongside run_name/config. Opaque
                passthrough — this generic leaf never interprets the keys (a tuning parent supplies
                task_ref/dataset_ref/reward_ref here); it only relays them into the envelope, keeping the leaf domain-agnostic
                (B7).
            platform_aux_input (CreateRunConfigRunDtoPlatformAuxInput | Unset): Optional second opaque JSON document,
                delivered only as a file mount inside the container workspace — never via the platform-input environment
                variable. Size-unbounded. Opaque passthrough like config: the platform never reads inside it. Requires a
                wrapper-run image to be read at all.
            env (CreateRunConfigRunDtoEnv | Unset): Composing-parent-supplied OS environment variables merged into the child
                container's real process environment. Applied before the run-config version's customer-secret-derived variables
                and before the platform-input environment variable, so this field can override neither.
            completion_mode (CreateRunConfigRunDtoCompletionMode | Unset): How handleTerminal classifies this run's terminal
                state. 'training' (default when omitted, matches this job type's original behavior): completed requires an
                ingested or output.json training-contract terminal document within the grace window — agent-service status alone
                is not sufficient. 'generic': completed is derived directly from the agent-service run status once terminal,
                with no training-contract document required — for containers (e.g. a bare coding agent) that never emit
                training-contract telemetry. Omitting the field is equivalent to 'training', preserving every historical row's
                behavior exactly.
     """

    run_config_version_id: UUID
    run_name: str
    config: CreateRunConfigRunDtoConfig
    timeout_seconds: int | Unset = UNSET
    platform_input_refs: CreateRunConfigRunDtoPlatformInputRefs | Unset = UNSET
    platform_aux_input: CreateRunConfigRunDtoPlatformAuxInput | Unset = UNSET
    env: CreateRunConfigRunDtoEnv | Unset = UNSET
    completion_mode: CreateRunConfigRunDtoCompletionMode | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_run_config_run_dto_config import CreateRunConfigRunDtoConfig # noqa: PLC0415
        from ..models.create_run_config_run_dto_env import CreateRunConfigRunDtoEnv # noqa: PLC0415
        from ..models.create_run_config_run_dto_platform_aux_input import CreateRunConfigRunDtoPlatformAuxInput # noqa: PLC0415
        from ..models.create_run_config_run_dto_platform_input_refs import CreateRunConfigRunDtoPlatformInputRefs # noqa: PLC0415
        run_config_version_id = str(self.run_config_version_id)

        run_name = self.run_name

        config = self.config.to_dict()

        timeout_seconds = self.timeout_seconds

        platform_input_refs: dict[str, Any] | Unset = UNSET
        if not isinstance(self.platform_input_refs, Unset):
            platform_input_refs = self.platform_input_refs.to_dict()

        platform_aux_input: dict[str, Any] | Unset = UNSET
        if not isinstance(self.platform_aux_input, Unset):
            platform_aux_input = self.platform_aux_input.to_dict()

        env: dict[str, Any] | Unset = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.to_dict()

        completion_mode: str | Unset = UNSET
        if not isinstance(self.completion_mode, Unset):
            completion_mode = self.completion_mode.value



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "runConfigVersionId": run_config_version_id,
            "runName": run_name,
            "config": config,
        })
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds
        if platform_input_refs is not UNSET:
            field_dict["platformInputRefs"] = platform_input_refs
        if platform_aux_input is not UNSET:
            field_dict["platformAuxInput"] = platform_aux_input
        if env is not UNSET:
            field_dict["env"] = env
        if completion_mode is not UNSET:
            field_dict["completionMode"] = completion_mode

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_run_config_run_dto_config import CreateRunConfigRunDtoConfig # noqa: PLC0415
        from ..models.create_run_config_run_dto_env import CreateRunConfigRunDtoEnv # noqa: PLC0415
        from ..models.create_run_config_run_dto_platform_aux_input import CreateRunConfigRunDtoPlatformAuxInput # noqa: PLC0415
        from ..models.create_run_config_run_dto_platform_input_refs import CreateRunConfigRunDtoPlatformInputRefs # noqa: PLC0415
        d = dict(src_dict)
        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        run_name = d.pop("runName")

        config = CreateRunConfigRunDtoConfig.from_dict(d.pop("config"))




        timeout_seconds = d.pop("timeoutSeconds", UNSET)

        _platform_input_refs = d.pop("platformInputRefs", UNSET)
        platform_input_refs: CreateRunConfigRunDtoPlatformInputRefs | Unset
        if isinstance(_platform_input_refs,  Unset):
            platform_input_refs = UNSET
        else:
            platform_input_refs = CreateRunConfigRunDtoPlatformInputRefs.from_dict(_platform_input_refs)




        _platform_aux_input = d.pop("platformAuxInput", UNSET)
        platform_aux_input: CreateRunConfigRunDtoPlatformAuxInput | Unset
        if isinstance(_platform_aux_input,  Unset):
            platform_aux_input = UNSET
        else:
            platform_aux_input = CreateRunConfigRunDtoPlatformAuxInput.from_dict(_platform_aux_input)




        _env = d.pop("env", UNSET)
        env: CreateRunConfigRunDtoEnv | Unset
        if isinstance(_env,  Unset):
            env = UNSET
        else:
            env = CreateRunConfigRunDtoEnv.from_dict(_env)




        _completion_mode = d.pop("completionMode", UNSET)
        completion_mode: CreateRunConfigRunDtoCompletionMode | Unset
        if isinstance(_completion_mode,  Unset):
            completion_mode = UNSET
        else:
            completion_mode = CreateRunConfigRunDtoCompletionMode(_completion_mode)




        create_run_config_run_dto = cls(
            run_config_version_id=run_config_version_id,
            run_name=run_name,
            config=config,
            timeout_seconds=timeout_seconds,
            platform_input_refs=platform_input_refs,
            platform_aux_input=platform_aux_input,
            env=env,
            completion_mode=completion_mode,
        )

        return create_run_config_run_dto

